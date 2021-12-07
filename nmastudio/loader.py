import pandas as pd
from storage import (NET_DATA, RANKING_DATA,
                     FUNNEL_DATA, FUNNEL_DATA_OUT2,
                     CONSISTENCY_DATA,
                     NETSPLIT_DATA, NETSPLIT_DATA_OUT2)
from nmastudio.tools.utils import _IS_JUPYTER, _IS_IPYTHON


class Loader:
    net_data = NET_DATA
    ranking_data = RANKING_DATA
    funnel_data = FUNNEL_DATA
    funnel_data_out2 = FUNNEL_DATA_OUT2
    consistency_data = CONSISTENCY_DATA
    net_split_data = NETSPLIT_DATA
    net_split_data_out2 = NETSPLIT_DATA_OUT2

    def __init__(self):
        self._is_jupyter = _IS_JUPYTER
        self._is_ipython = _IS_IPYTHON

    def _load_long(self):
        """Load format long format."""
        pass

    def _load_contrast(self):
        """Load contrast format."""
        pass


    def _load_iv(self, path, binary):
        """Load format inverse variancee (IV)."""
        self.data = pd.read_csv(path)


    def _run_checks(self):
        pass


    def consistency_checks(self, netsplit=False, outcome=False, edges=None):
        if netsplit:
            df = (self.net_split_data if not outcome
                  else self.net_split_data_out2
            if self.net_split_data_out2 else None)
            if df is not None:
                comparisons = df.comparison.str.split(':', expand=True)
                df['Comparison'] = comparisons[0] + ' vs ' + comparisons[1]
                df = df.loc[:, ~df.columns.str.contains("comparison")]
                df = df.sort_values(by='Comparison').reset_index()
                df = df[['Comparison', "direct", "indirect", "p-value"]].round(decimals=4)

            slctd_comps = []
            for edge in edges or []:
                src, trgt = edge['source'], edge['target']
                slctd_comps += [f'{src} vs {trgt}']
            if edges and df is not None:
                df = df[df.Comparison.isin(slctd_comps)]
            return df
        else:
            return self.consistency_data.round(decimals=4)

if __name__ == '__main__':
    path = 'db/psoriasis_wide.csv'
