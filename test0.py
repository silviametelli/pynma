

def test_import_package():
    import nmastudio
    nma = nmastudio.NMA()
    assert nma

import nmastudio

def test_plotting():
    nma = nmastudio.NMA()
    nma.league_table(subset=['BRODA', 'ETA', 'FUM'], values_only=True)
    assert False

def test_table():
    nma = nmastudio.NMA()
    nma.league_table(subset=['BRODA', 'ETA', 'FUM'], values_only=True)
