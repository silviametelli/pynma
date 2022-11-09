import pandas as pd, numpy as np, plotly, os
import nmastudio
import ipycytoscape, json, webbrowser
from nmastudio.tools.utils import get_network
from ipywidgets.embed import embed_minimal_html
from nmastudio._plotting_functions.cytoscape_styleesheeet import get_stylesheet
NET_DATA = pd.read_csv('db/psoriasis_wide.csv')
DEFAULT_ELEMENTS = get_network(df=NET_DATA)

from nmastudio.loader import Loader
import nmastudio._plotting_functions
from nmastudio.tools.utils import _IS_JUPYTER

if _IS_JUPYTER:
    from IPython.core.display import HTML

flatten = lambda t: [item for sublist in t for item in sublist]


DEBUG = True
if DEBUG:
    class Empty: pass
    self = Empty()


class NMA(Loader):

    def __init__(self):
        super().__init__()  # import attributes from Loader class

    def print_summary(self):
        """"
        Print main network characteristics:
        1) number of studies
        2) number of treatments
        3) number of variables in data
        """
        COLUMN_NAMES = ['Number of studies', 'Number of treatments', 'Number of variables']
        data = self.net_data
        uniquetrts = np.unique(data[['treat1', 'treat2']].dropna().values.flatten())
        n_stud = len(np.unique(data.studlab))
        n_trts = len(uniquetrts)
        n_vars = len(data.columns)
        values = [n_stud, n_trts, n_vars]
        summary_dict = {col: val for col, val in zip(COLUMN_NAMES,values)}
        summary = pd.DataFrame(data=summary_dict, index=[0])
        trts_df = pd.DataFrame(uniquetrts, columns=["Treatments"])
        trts_df.index += 1 # treatment index from one: more intuitive for users
        return summary.reset_index(drop=True), trts_df



    def plot_network(self, layout='circle', pie=False, height=None, width=None):
        """
        Notes
        -----
        May have reduced functionalities when NOT opened from jupyter.
        Parameters
        ----------
        layout : str
            Cytoscape network layout - e.g. circle, cola, grid, breadthfirst, concentric, dagre, random,  etc.
        pie : bool
            Whether to include pie chart in nodes (according to associated rob)
        height : str
            Interactive widget height; e.g. '400px'
        width : str
            Interactive widget width; e.g. '400px'
        Returnss
        -------
        ipycytoscape.cytoscape.CytoscapeWidget
        """
        cyG = ipycytoscape.CytoscapeWidget(cytoscape_layout={'name': layout})
        cy_edges, cy_nodes = get_network(self.net_data, sep=True)
        cyG.graph.add_graph_from_json({'nodes':cy_nodes, 'edges':cy_edges})
        cyG.set_style(get_stylesheet(pie=pie))
        if height: cyG.layout.height = '200px'
        if width: cyG.layout.width = '800px'
        if self._is_jupyter:
            return cyG
        else:
            _net_plot_path = 'nmastudio/__temp/export.html'
            embed_minimal_html(_net_plot_path, views=[cyG], title='NMA Studio - Treatments network')
            webbrowser.open(f'file://{os.getcwd()}/{_net_plot_path}', new=2)


    def plot_nma_forests(self, type="nma", outcome2=False, node_ref=None, edge_ref=None):
        """
        Notes
        -----
        Parameters
        ----------
        type : str
            Type of forest plot desired:
                "nma" for NMA forest plot
                "pw" for pairwise forest plot
                "bidim" for bi-dimensional forest plot
        outcome2 : bool
            Whether to show results for second outcome
        node_ref : str
            Reference node
        edge_ref : str
            Reference edge

        """
        if type == 'nma':
            fig = nmastudio._plotting_functions._nma_forest(node_ref=node_ref, forest_data=self.forest_data, forest_data_out2=self.funnel_data_out2)
        elif type == 'bidim':
            fig = nmastudio._plotting_functions._bidim_forest(node_ref=node_ref,forest_data=self.forest_data, forest_data_out2=self.funnel_data_out2)
        elif type == 'pw':
            fig = nmastudio._plotting_functions._pw_forest(edge_ref=edge_ref, forest_data_prws=self.forest_data_pw, forest_data_prws_out_2=self.forest_data_pw_out2)
        else:
            raise KeyError("type must be either nma, bidim or pw.")

        if not self._is_jupyter:
            plotly.offline.plot(fig)
        return fig



    def league_table(self, subset=None, values_only=False, lower_error=False, upper_error=False):
        """
        Notes
        -----
        Parameters
        ----------
        subset : list
            Subset of nodes to be displayed in the table
        values_only : bool
          shows only point estimates (CIs not printed)
        lower_error : str
            shows lower confidence bound only
        upper_error : bool
            shows upper confidence bound only

        """
        return nmastudio._plotting_functions._print_league_table(self.net_data, self.league_table_data,
                                                                 subset=subset,
                                                                 values_only=values_only,
                                                                 lower_error=lower_error,
                                                                 upper_error=upper_error)



    def plot_funnels(self, node_ref, outcome2=False):
        """
        Notes: comparisons involving one study removed
        -----
        Parameters
        ----------
        node_ref : str
            Reference node
        outcome2 : bool
            Whether to show results for second outcome
        """
        fig = nmastudio._plotting_functions._funnelplot(node_ref=node_ref,
                                                        funnel_data=self.funnel_data,
                                                        funnel_data_out2=self.funnel_data_out2)
        if not self._is_jupyter:
            plotly.offline.plot(fig)
        return fig



    def consistency_checks(self, type="netsplit", outcome2=False, subset=None):
        """
        Parameters
        ----------
        netsplit: str
            Type of consistency check desired:
                "netsplit" for local netsplit approach
                "design" for global design-by-treatment interaction method
        outcome2 : bool
            Whether to show results for second outcome
        subset: list
            Subset of edges to be displayed in the netsplit table
        """
        if type=='netsplit':
            df = (self.net_split_data if not outcome2
                  else self.net_split_data_out2
            if self.net_split_data_out2 else None)
            if df is not None:
                comparisons = df.comparison.str.split(':', expand=True)
                df['Comparison'] = comparisons[0] + ' vs ' + comparisons[1]
                df = df.loc[:, ~df.columns.str.contains("comparison")]
                df = df.sort_values(by='Comparison').reset_index()
                df = df[['Comparison', "direct", "indirect", "p-value"]].round(decimals=4)

            slctd_comps = []
            for edge in subset or []:
                src, trgt = edge['source'], edge['target']
                slctd_comps += [f'{src} vs {trgt}']
            if subset and df is not None:
                df = df[df.Comparison.isin(slctd_comps)]
            return df
        elif type=='design':
            return self.consistency_data.round(decimals=4)
        else:
            raise KeyError("type must be either netsplit or design.")


    def plot_ranking(self, type='heatmap', outcome2=False):
        """
        Notes
        -----
        Parameters
        ----------
        type: str
            Type of ranking plot to be displayed:
                "heatmap" of p-scores
                "scatter" for scatter plot of p-scores (if both outcomes)
        outcome2 : bool
           if True, shows results for both first and second outcome else first outcome only

        """
        if type == 'scatter':
            fig = nmastudio._plotting_functions._ranking_scatter(self.net_data, self.ranking_data)
        elif type == 'heatmap':
            fig = nmastudio._plotting_functions._ranking_heatmap(self.ranking_data)
        else:
            raise KeyError("type must be either heatmap or scatter.")

        if not self._is_jupyter:
            plotly.offline.plot(fig)
        return fig



    def __repr__(self):
        """ Representation string """
        sb, eb = ("\033[1m","\033[0;0m") if self._is_ipython else ('','')  # Bold
        sr, er = ("\x1b[31m", "\x1b[0m") if self._is_ipython else ('','')  # Red
        sg, eg = ("\033[92m", "\033[0m") if self._is_ipython else ('','')  # Green
        _repr = f"\n{sb}NMA Studio{eb}"
        return _repr

    def _repr_html_(self):
        with open(f'nmastudio/__res/icon_mini.svg', 'r') as f:
            _svg_cnn = f.read()
        html_repr = _svg_cnn + f"""</br>
        <span style="white-space: nowrap;">
        <b>Dataset</b>:
        <span style="color:green; 
                     background-color:red"; 
        white-space: nowrap;>{'Default' if self._states['data']=='default' else 'User upload'}</span>
        </span></br>
        <span style="white-space: nowrap;">
        <span style="color: gray">Engine:</span>
        <span white-space: nowrap;>Engine</span>
        </span></br>
        <span style="white-space: nowrap;">
        <span style="color: gray">Selected database:</span>
        <span white-space: nowrap;>{self._states['data']}</span>
        </span></br>
        </br>
        <span style="white-space: nowrap;">
        <b>Summary of the NMA data</b></br>
        {self.print_summary()[0].to_html()} 
        </br>
        <b>Available methods</b>:</br>
        <span white-space: nowrap;>plot_network(<span style="color: orange">layout</span>='circle', 
        <span style="color: orange">pie</span>=False, <span style="color: orange">height</span>=None, 
        <span style="color: orange">width</span>=None)</span></br>
        <span white-space: nowrap;>plot_forest()</span></br>
        <span white-space: nowrap;>plot_funnels(node_ref)</span></br>
        <span white-space: nowrap;>plot_ranking(type='heatmap', outcomes=None)</span></br>
        <span white-space: nowrap;>plot_funnels(node_ref)</span></br>
        <span white-space: nowrap;>league_table(subset=None, values_only=False, lower_error=False, upper_error=False)</span>
        """
        # display(HTML(html_repr))
        return html_repr

    # def __str__(self):
    #     return self._repr_html_()


############################################################################################################################
##############################################################  MAIN #######################################################
############################################################################################################################


if __name__=='__main__':
    path = 'db/psoriasis_wide.csv'
    self = NMA()
    self.league_table(subset=['BRODA', 'ETA', 'FUM'], values_only=True)
    self.plot_network(pie=True, layout='grid')
    # self.plot_ranking(type='heatmap')



