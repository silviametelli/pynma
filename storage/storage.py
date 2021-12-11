import os

import pandas as pd
from nmastudio.tools.utils import get_network
import warnings
warnings.filterwarnings('ignore')

_DB_PATH = './db'
print(os.getcwd())

NET_DATA = pd.read_csv(f'{_DB_PATH}/psoriasis_wide.csv')
NET_DATA2 = NET_DATA.drop(["TE", "seTE", "n1", "n2"], axis=1)
NET_DATA2 = NET_DATA2.rename(columns={"TE2": "TE", "seTE2": "seTE", "n2.1": "n1", "n2.2": "n2"})
CONSISTENCY_DATA = pd.read_csv(f'{_DB_PATH}/consistency/consistency.csv')
DEFAULT_ELEMENTS = USER_ELEMENTS = get_network(df=NET_DATA)
DEFAULT_ELEMENTS2 = USER_ELEMENTS2 = get_network(df=NET_DATA2)
FOREST_DATA = pd.read_csv(f'{_DB_PATH}/forest_data/forest_data.csv')
FOREST_DATA_OUT2 = pd.read_csv(f'{_DB_PATH}/forest_data/forest_data_outcome2.csv')
FOREST_DATA_PRWS = pd.read_csv(f'{_DB_PATH}/forest_data/forest_data_pairwise.csv')
FOREST_DATA_PRWS_OUT2 = pd.read_csv(f'{_DB_PATH}/forest_data/forest_data_pairwise_out2.csv')
LEAGUE_TABLE_DATA = pd.read_csv(f'{_DB_PATH}/league_table_data/league_table.csv', index_col=0)
CINEMA_NET_DATA1 =  pd.read_csv(f'{_DB_PATH}/Cinema/cinema_report_PASI90.csv')
CINEMA_NET_DATA2 =  pd.read_csv(f'{_DB_PATH}/Cinema/cinema_report_SAE.csv')
NETSPLIT_DATA =  pd.read_csv(f'{_DB_PATH}/consistency/consistency_netsplit.csv')
NETSPLIT_DATA_OUT2 =  pd.read_csv(f'{_DB_PATH}/consistency/consistency_netsplit_out2.csv')
NETSPLIT_DATA_ALL =  pd.read_csv(f'{_DB_PATH}/consistency/netsplit_all.csv')
NETSPLIT_DATA_ALL_OUT2 =  pd.read_csv(f'{_DB_PATH}/consistency/netsplit_all_out2.csv')
RANKING_DATA = pd.read_csv(f'{_DB_PATH}/ranking/rank.csv')
FUNNEL_DATA = pd.read_csv(f'{_DB_PATH}/funnel/funnel_data.csv')
FUNNEL_DATA_OUT2 = pd.read_csv(f'{_DB_PATH}/funnel/funnel_data_out2.csv')


for v in ['NET_DATA', 'NET_DATA2', 'NET_DATA2', 'CONSISTENCY_DATA', 'DEFAULT_ELEMENTS',
          'DEFAULT_ELEMENTS2', 'FOREST_DATA', 'FOREST_DATA_OUT2', 'FOREST_DATA_PRWS',
          'FOREST_DATA_PRWS_OUT2', 'LEAGUE_TABLE_DATA', 'CINEMA_NET_DATA1',
          'CINEMA_NET_DATA2', 'NETSPLIT_DATA', 'NETSPLIT_DATA_OUT2', 'NETSPLIT_DATA_ALL',
          'NETSPLIT_DATA_ALL_OUT2', 'RANKING_DATA', 'FUNNEL_DATA', 'FUNNEL_DATA_OUT2']:
    exec(f"{v.lower()}={v}")