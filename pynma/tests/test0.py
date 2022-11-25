###################
#### nmastudio ####
#### testing ######
###################


def test_import_package():
    import pynma
    nma = pynma.NMA()
    assert nma

import pynma

def test_plotting():
    nma = pynma.NMA()
    nma.league_table(subset=['BRODA', 'ETA', 'FUM'], values_only=True)

def test_table():
    nma = pynma.NMA()
    nma.league_table(subset=['BRODA', 'ETA', 'FUM'], values_only=True)
