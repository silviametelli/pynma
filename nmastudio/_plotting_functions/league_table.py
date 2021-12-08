import numpy as np, pandas as pd
import plotly.graph_objects as go
import plotly
from nmastudio.tools.utils import _IS_JUPYTER

from nmastudio.tools.utils import CINEMA_g, CINEMA_y, CINEMA_lb, CINEMA_r, CLR_BCKGRND2, CX1, CX2


def _print_league_table(net_data, league_table_data, toggle_cinema=False,
                  cinema_net_data1=None, cinema_net_data2=None, subset=None):

    YEARS_DEFAULT = np.array([1963, 1990, 1997, 2001, 2003, 2004, 2005, 2006, 2007, 2008, 2010,
                              2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])
    leaguetable = league_table_data
    confidence_map = {k: n for n, k in enumerate(['low', 'medium', 'high'])}
    treatments = np.unique(net_data[['treat1', 'treat2']].dropna().values.flatten())
    robs = (net_data.groupby(['treat1', 'treat2']).rob.mean().reset_index()
            .pivot_table(index='treat2', columns='treat1', values='rob')
            .reindex(index=treatments, columns=treatments, fill_value=np.nan))
    if subset:
        leaguetable = leaguetable.loc[subset, subset]
        robs = robs.loc[subset, subset]

    if _IS_JUPYTER:
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
        return leaguetable


