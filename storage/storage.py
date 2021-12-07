import pandas as pd
from nmastudio.tools.utils import get_network
import warnings
warnings.filterwarnings('ignore')



NET_DATA = pd.read_csv('db/psoriasis_wide.csv')
NET_DATA2 = NET_DATA.drop(["TE", "seTE", "n1", "n2"], axis=1)
NET_DATA2 = NET_DATA2.rename(columns={"TE2": "TE", "seTE2": "seTE", "n2.1": "n1", "n2.2": "n2"})
CONSISTENCY_DATA = pd.read_csv('db/consistency/consistency.csv')
DEFAULT_ELEMENTS = USER_ELEMENTS = get_network(df=NET_DATA2)
DEFAULT_ELEMENTS2 = USER_ELEMENTS2 = get_network(df=NET_DATA2)
FOREST_DATA = pd.read_csv('db/forest_data/forest_data.csv')
FOREST_DATA_OUT2 = pd.read_csv('db/forest_data/forest_data_outcome2.csv')
FOREST_DATA_PRWS = pd.read_csv('db/forest_data/forest_data_pairwise.csv')
FOREST_DATA_PRWS_OUT2 = pd.read_csv('db/forest_data/forest_data_pairwise_out2.csv')
LEAGUE_TABLE_DATA = pd.read_csv('db/league_table_data/league_table.csv', index_col=0)
CINEMA_NET_DATA1 =  pd.read_csv('db/Cinema/cinema_report_PASI90.csv')
CINEMA_NET_DATA2 =  pd.read_csv('db/Cinema/cinema_report_SAE.csv')
NETSPLIT_DATA =  pd.read_csv('db/consistency/consistency_netsplit.csv')
NETSPLIT_DATA_OUT2 =  pd.read_csv('db/consistency/consistency_netsplit_out2.csv')
NETSPLIT_DATA_ALL =  pd.read_csv('db/consistency/netsplit_all.csv')
NETSPLIT_DATA_ALL_OUT2 =  pd.read_csv('db/consistency/netsplit_all_out2.csv')
RANKING_DATA = pd.read_csv('db/ranking/rank.csv')
FUNNEL_DATA = pd.read_csv('db/funnel/funnel_data.csv')
FUNNEL_DATA_OUT2 = pd.read_csv('db/funnel/funnel_data_out2.csv')


