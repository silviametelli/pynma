import numpy as np, pandas as pd
import plotly.graph_objects as go
import plotly
from pynma.tools.utils import _IS_JUPYTER

from pynma.tools.utils import CINEMA_g, CINEMA_y, CINEMA_lb, CINEMA_r, CLR_BCKGRND2, CX1, CX2


def _print_league_table(net_data, league_table_data, toggle_cinema=False,
                        cinema_net_data1=None, cinema_net_data2=None, subset=None,
                        values_only=False, lower_error=False, upper_error=False):

    YEARS_DEFAULT = np.array([1963, 1990, 1997, 2001, 2003, 2004, 2005, 2006, 2007, 2008, 2010,
                              2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])
    leaguetable = league_table_data
    if sum([values_only, lower_error, upper_error])>1:
        raise AssertionError("Only one of values_only, lower_error, upper_error can be specified at a time")
    if values_only:   clean_content = lambda e: e.split('\n')[0]
    elif lower_error: clean_content = lambda e: (e.split('\n')[-1].replace('(', '')
                                                  .replace(')', '').replace(' ', '')
                                                  .split(',')[0])
    elif upper_error: clean_content = lambda e: (e.split('\n')[-1].replace('(', '')
                                                  .replace(')', '').replace(' ', '')
                                                  .split(',')[-1])
    else:             clean_content = lambda e: e


    leaguetable = leaguetable.applymap(clean_content)

    if any((values_only, lower_error, upper_error)):
        np.fill_diagonal(leaguetable.values, [np.nan] * len(leaguetable))
        leaguetable = leaguetable.astype(np.float64)

    confidence_map = {k: n for n, k in enumerate(['low', 'medium', 'high'])}
    treatments = np.unique(net_data[['treat1', 'treat2']].dropna().values.flatten())
    robs = (net_data.groupby(['treat1', 'treat2']).rob.mean().reset_index()
            .pivot_table(index='treat2', columns='treat1', values='rob')
            .reindex(index=treatments, columns=treatments, fill_value=np.nan))
    if subset:

        tril_order = pd.DataFrame(np.tril(np.ones(leaguetable.shape)),
                                      columns=leaguetable.columns,
                                      index=leaguetable.columns)
        tril_order = tril_order.loc[subset, subset]
        filter = np.tril(tril_order==0)
        filter += filter.T # Rubbish inverting of rows and columns common in meta-analysis visualization

        leaguetable = leaguetable.loc[subset, subset]
        leaguetable = leaguetable.loc[subset, subset]
        leaguetable_values = leaguetable.values
        leaguetable_values[filter] = leaguetable_values.T[filter]
        leaguetable = pd.DataFrame(leaguetable_values,
                                       columns=leaguetable.columns,
                                       index=leaguetable.columns)

        robs = robs.loc[subset, subset]
        robs_values = robs.values
        robs_values[filter] = robs_values.T[filter]
        robs = pd.DataFrame(robs_values,
                                columns=robs.columns,
                                index=robs.columns)

        treatments = subset

    if _IS_JUPYTER:
        if any((values_only, lower_error, upper_error)):
            leaguetable = leaguetable.round(3).astype(str)
            np.fill_diagonal(leaguetable.values, leaguetable.columns)
        # for row hover use <tr> instead of <td>
        cell_hover = {'selector': 'td:hover',
                      'props': [('background-color', '#ffffb3')]}
        index_names = {'selector': '.index_name',
                       'props': 'font-style: italic; color: darkgrey; font-weight:normal;'}
        headers = {'selector': 'th:not(.index_name)',
                   'props': 'background-color: #000066; color: white;'}
        color_cells = (lambda x: f"background-color: {CINEMA_g}" if x <= 1
        else f"background-color: {CINEMA_y}" if x <= 2
        else f"background-color: {CINEMA_r}" if x > 2
        else f"background-color: None")
        return (leaguetable.style.apply(lambda x: robs.applymap(color_cells), axis=None)
         .set_table_styles([cell_hover, index_names, headers])
         .set_properties(**{'max-width': '800px', 'width': '800px'})
         .set_tooltips(robs, props="""visibility: hidden; position: absolute; z-index: 1; border: 1px solid #000066;
                                      background-color: grey; color: black; font-size: 2em; 
                                      transform: translate(0px, -24px); padding: 0.6em; border-radius: 0.5em;""")
         )
    else:
        if not any((values_only, lower_error, upper_error)):
            for c in leaguetable:
                leaguetable[c] = leaguetable[c].str.replace('\n', ' ')
        return leaguetable


