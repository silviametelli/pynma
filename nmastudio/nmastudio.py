import pandas as pd, numpy as np, plotly, os

import nmastudio

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
        with open(f'nmastudio/__res/icon_tiny.svg', 'r') as f:
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

    def __str__(self):
        return self._repr_html_()




if __name__=='__main__':
    path = 'db/psoriasis_wide.csv'
    self = NMA()
    self.league_table(values_only=True)
    # self.plot_ranking(type='heatmap')



