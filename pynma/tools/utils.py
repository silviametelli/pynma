import numpy as np, pandas as pd
import rpy2
from rpy2.robjects import pandas2ri  # Define the R script and loads the instance in Python
#pandas2ri.activate()
import rpy2.robjects as ro
import rpy2.rinterface_lib as rlib
from rpy2.robjects.conversion import localconverter

#  customised colors
CINEMA_g, CINEMA_y, CINEMA_lb, CINEMA_r = '#5aa469', '#f8d49d', '#75cfb8', '#d35d6e'
CLR_BCKGRND = '#1b242b'
CLR_BCKGRND_old = '#1b242b'
CLR_BCKGRND2 = '#40515e'
CLR_BORDEAUX = '#751226'
CLR_BCKGRND_TABS = '#6f8ba1'
DFLT_ND_CLR = '#07ABA0'
DFLT_EDG_CLR = '#b2b2b2'

CX1 = '#1A242B'
CX2 = '#d6d6d6'

# ------------------------------------------------------------------ detect Jupyter # -------------------------------------------------------------- #

try:    # This works on jupyter ipython
    _IS_JUPYTER = bool(get_ipython().config)
    _IS_IPYTHON = True
except: # On plain python get_ipython is not defined
    _IS_JUPYTER = _IS_IPYTHON =  False


# -------------------------------------------------------------------- network plot ----------------------------------------------------------------- #

CMAP = ['bisque', 'gold', 'light blue', 'tomato', 'orange', 'olivedrab', 'darkslategray', 'orchid', 'brown', 'navy',
        'palegreen', 'black', 'brown', 'green']
def get_network(df, sep=False):
    df = df.dropna(subset=['TE', 'seTE'])
    if "treat1_class" and "treat2_class" in df.columns:
        df_treat = df.treat1.dropna().append(df.treat2.dropna()).reset_index(drop=True)
        df_class = df.treat1_class.dropna().append(df.treat2_class.dropna()).reset_index(drop=True)
        long_df_class = pd.concat([df_treat,df_class], axis=1).reset_index(drop=True)
        long_df_class = long_df_class.rename({long_df_class.columns[0]: 'treat', long_df_class.columns[1]: 'class'}, axis='columns')
        long_df_class['class'].replace(dict(zip(long_df_class['class'], [int(x-1) for x in long_df_class['class']])), inplace=True)
        all_nodes_class = long_df_class.drop_duplicates().sort_values(by='treat').reset_index(drop=True)
        num_classes = all_nodes_class['class'].max()+1 #because all_nodes_class was shifted by minus 1
    sorted_edges = np.sort(df[['treat1', 'treat2']], axis=1)  ## removes directionality
    df.loc[:,['treat1', 'treat2']] = sorted_edges
    edges = df.groupby(['treat1', 'treat2']).TE.count().reset_index()
    df_n1g = df.rename(columns={'treat1': 'treat', 'n1':'n'}).groupby(['treat'])
    df_n2g = df.rename(columns={'treat2': 'treat', 'n2':'n'}).groupby(['treat'])
    df_n1, df_n2 = df_n1g.n.sum(), df_n2g.n.sum()
    all_nodes_sized = df_n1.add(df_n2, fill_value=0)
    df_n1, df_n2 = df_n1g.rob.value_counts(), df_n2g.rob.value_counts()
    all_nodes_robs = df_n1.add(df_n2, fill_value=0).rename(('count')).unstack('rob', fill_value=0)
    all_nodes_sized = pd.concat([all_nodes_sized, all_nodes_robs], axis=1).reset_index()
    if "treat1_class" and "treat2_class" in df.columns: all_nodes_sized = pd.concat([all_nodes_sized, all_nodes_class['class']], axis=1).reset_index(drop=True)
    for c in {1,2,3}.difference(all_nodes_sized): all_nodes_sized[c] = 0
    cy_edges = [{'data': {'source': source,  'target': target,
                          'weight': weight * 1, 'weight_lab': weight}}
                for source, target, weight in edges.values]
    max_trsfrmd_size = np.sqrt(all_nodes_sized.iloc[:,1].max()) / 70
    if "treat1_class" and "treat2_class" in df.columns:
        cy_nodes = [{"data": {"id": target,
                          "label": target,
                          "n_class": num_classes,
                          'size': np.sqrt(size)/max_trsfrmd_size,
                          'pie1': r1/(r1+r2+r3), 'pie2':r2/(r1+r2+r3), 'pie3': r3/(r1+r2+r3),
                          }, 'classes': f'{CMAP[cls]}'} for target, size, r1, r2, r3, cls in all_nodes_sized.values]
    else:
        cy_nodes = [{"data": {"id": target,
                          "label": target,
                          'classes':'genesis',
                          'size': np.sqrt(size)/max_trsfrmd_size,
                          'pie1': r1/(r1+r2+r3),
                          'pie2':r2/(r1+r2+r3),
                          'pie3': r3/(r1+r2+r3)}} for target, size, r1, r2, r3 in all_nodes_sized.values]
    if sep:
        return cy_edges, cy_nodes
    else:
        return cy_edges + cy_nodes


# ------------------------------------------------------ adjust data ------------------------------------------------------------------------- #

r = ro.r
r['source']('R_Codes/all_R_functions.R')  # Loading the function we have defined in R.
run_NetMeta_r = ro.globalenv['run_NetMeta']  # Get run_NetMeta from R
league_table_r = ro.globalenv['league_rank']  # Get league_table from R
pairwise_forest_r = ro.globalenv['pairwise_forest']  # Get pairwise_forest from R
funnel_plot_r = ro.globalenv['funnel_funct']  # Get pairwise_forest from R
run_pairwise_data_long_r = ro.globalenv['get_pairwise_data_long']  # Get pairwise data from long format from R
run_pairwise_data_contrast_r = ro.globalenv['get_pairwise_data_contrast']  # Get pairwise data from contrast format from R



def apply_r_func(func, df):

    with localconverter(ro.default_converter + pandas2ri.converter):
        df_r = ro.conversion.py2rpy(df.reset_index(drop=True))
    func_r_res = func(dat=df_r)
    r_result = pandas2ri.rpy2py(func_r_res)

    if isinstance(r_result, ro.vectors.ListVector):
        with localconverter(ro.default_converter + pandas2ri.converter):
            leaguetable, pscores, consist, netsplit, netsplit_all  = (ro.conversion.rpy2py(rf) for rf in r_result)
        return leaguetable, pscores, consist, netsplit, netsplit_all
    else:
        df_result = r_result.reset_index(drop=True)  # Convert back to a pandas.DataFrame.
        return df_result


def apply_r_func_two_outcomes(func, df):
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_r = ro.conversion.py2rpy(df.reset_index(drop=True))
    func_r_res = func(dat=df_r, outcome2=True)
    r_result = pandas2ri.rpy2py(func_r_res)

    if isinstance(r_result, ro.vectors.ListVector):
        with localconverter(ro.default_converter + pandas2ri.converter):
            leaguetable, pscores, consist, netsplit, netsplit2, netsplit_all, netsplit_all2 = (ro.conversion.rpy2py(rf) for rf in r_result)
        return leaguetable, pscores, consist, netsplit, netsplit2, netsplit_all, netsplit_all2
    else:
        df_result = r_result.reset_index(drop=True)  # Convert back to a pandas.DataFrame.
        return df_result


def adjust_data(data, dataselectors, value_format, value_outcome1, value_outcome2):

    if data['rob'].dtype == object:
        data['rob'] = (data['rob'].str.lower()
                      .replace({'low': 'l', 'medium': 'm', 'high': 'h'})
                      .replace({'l': 1, 'm': 2, 'h': 3}))
    data['effect_size1'] = dataselectors[0]

    if value_format=='long':
        for c in data.columns:
            if data[c].dtype == object:
                data[c].fillna('__NONE__', inplace=True)
        if value_outcome2:
            data['effect_size2'] = dataselectors[1]
            data = apply_r_func_two_outcomes(func=run_pairwise_data_long_r, df=data)
        else:
            data = apply_r_func(func=run_pairwise_data_long_r, df=data)
        data[data=='__NONE__'] = np.nan


    if value_format=='contrast':
        for c in data.columns:
            if data[c].dtype == object:
                data[c].fillna('__NONE__', inplace=True)
        if value_outcome2:
            data['effect_size2'] = dataselectors[1]
            data = apply_r_func_two_outcomes(func=run_pairwise_data_contrast_r, df=data)
        else:
            data = apply_r_func(func=run_pairwise_data_contrast_r, df=data)
        data[data=='__NONE__'] = np.nan

    if value_format == 'iv':
        data['effect_size1'] = dataselectors[0]
        if value_outcome2: data['effect_size2'] = dataselectors[1]
        data = data

    return data





