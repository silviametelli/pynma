import os, shutil
import pandas as pd, numpy as np
from pynma.tools.utils import adjust_data


from storage import (NET_DATA, RANKING_DATA,
                     FUNNEL_DATA, FUNNEL_DATA_OUT2,
                     CONSISTENCY_DATA,
                     NETSPLIT_DATA, NETSPLIT_DATA_OUT2,
                     LEAGUE_TABLE_DATA, FOREST_DATA, FOREST_DATA_OUT2,
                     FOREST_DATA_PRWS, FOREST_DATA_PRWS_OUT2)
from pynma.tools.utils import _IS_JUPYTER, _IS_IPYTHON, adjust_data, get_network

class Loader:
    net_data = NET_DATA
    ranking_data = RANKING_DATA
    funnel_data = FUNNEL_DATA
    funnel_data_out2 = FUNNEL_DATA_OUT2
    consistency_data = CONSISTENCY_DATA
    net_split_data = NETSPLIT_DATA
    net_split_data_out2 = NETSPLIT_DATA_OUT2
    league_table_data = LEAGUE_TABLE_DATA
    forest_data = FOREST_DATA
    forest_data2 = FOREST_DATA_OUT2
    forest_data_pw = FOREST_DATA_PRWS
    forest_data_pw_out2 = FOREST_DATA_PRWS_OUT2


    def __init__(self):
        self._states = dict(data='default')
        __TEMP_PATH = 'pynma/__temp'
        if os.path.exists(__TEMP_PATH):
            shutil.rmtree(__TEMP_PATH)
        os.makedirs(__TEMP_PATH, exist_ok=True)
        self._is_jupyter = _IS_JUPYTER
        self._is_ipython = _IS_IPYTHON



    def _load_long(self):
        """Load long format."""
        pass



    def _load_contrast(self):
        """Load contrast format."""
        pass



    def _load_iv(self, path, binary):
        """Load data in inverse variance format (iv)."""
        self.data = pd.read_csv(path)



    def adjust_data(self):
        pass


    def _run_checks(self):
        pass


#################################### MAIN ####################################

if __name__ == '__main__':
    path = 'db/psoriasis_wide.csv'
