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

DEBUG = True
if DEBUG:
    class Empty: pass
    self = Empty()


class NMA(Loader):

    def plot_network(self, layout='circle', pie=False, height=None, width=None):
        """
        Notes
        -----
        Reduced functionalities when NOT opened from jupyter.

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

        Returns
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


    def plot_forest(self):
        pass

    def plot_funnels(self, node_ref):
        fig = nmastudio._plotting_functions._funnelplot(node_ref=node_ref,
                                                        funnel_data=self.funnel_data,
                                                        funnel_data_out2=self.funnel_data_out2)
        if not self._is_jupyter:
            plotly.offline.plot(fig)
        return fig

    def plot_ranking(self, type='heatmap', outcomes=None):

        if type=='scatter':
            fig = nmastudio._plotting_functions._ranking_scatter(self.net_data, self.ranking_data)
        elif type=='heatmap':
            fig = nmastudio._plotting_functions._ranking_heatmap(self.ranking_data)
        else:
            raise KeyError("type must be either heatmap or scatter.")

        if not self._is_jupyter:
            plotly.offline.plot(fig)
        return fig

    def league_table(self, subset=None, values_only=False, lower_error=False, upper_error=False):
        return nmastudio._plotting_functions._print_league_table(self.net_data, self.league_table_data,
                                                                 subset=subset,
                                                                 values_only=values_only,
                                                                 lower_error=lower_error,
                                                                 upper_error=upper_error)


    def __repr__(self):
        sb, eb = ("\033[1m","\033[0;0m") if self._is_ipython else ('','')  # Bold
        sr, er = ("\x1b[31m", "\x1b[0m") if self._is_ipython else ('','')  # Red
        sg, eg = ("\033[92m", "\033[0m") if self._is_ipython else ('','')  # Green
        _repr = f"\n{sb}NMA Studio{eb}"
        return _repr

    def _repr_html_(self):
        # path = f'{os.path.dirname(__file__)}/__res/icon.ico'
        with open(f'nmastudio/__res/icon_mini.svg', 'r') as f:
            _svg_cnn = f.read()
        html_repr = _svg_cnn + f"""</br>
        <span style="white-space: nowrap;">
        <b>DISC connection</b>:
        <span style="color:green; 
                     background-color:red"; 
        white-space: nowrap;>Active</span>
        </span></br>
        <span style="white-space: nowrap;">
        <span style="color: gray">Engine:</span>
        <span white-space: nowrap;>Engine</span>
        </span></br>
        <span style="white-space: nowrap;">
        <span style="color: gray">Selected database:</span>
        <span white-space: nowrap;>db</span>
        </span></br>
        </br>
        <span style="white-space: nowrap;">
        <b>Spark Connection</b>:
        <span style="color:green;
                            background-color:red"; 
        white-space: nowrap;>XXX</span>
        </span>"""
        # display(HTML(html_repr))
        return html_repr

    # def __str__(self):
    #     return self._repr_html_()




if __name__=='__main__':
    path = 'db/psoriasis_wide.csv'
    self = NMA()
    self.league_table(subset=['BRODA', 'ETA', 'FUM'], values_only=True)
    self.plot_network(pie=True, layout='grid')
    # self.plot_ranking(type='heatmap')



