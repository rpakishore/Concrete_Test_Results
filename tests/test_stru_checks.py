from conc_test_report.stru_checks import *

def test_slump():
    assert slump(1, 2, 3.) == 1
    assert slump(2, 2, 3.) == 0
    assert slump(2.1, 2, 3.) == 0
    assert slump(3, 2, 3.) == 0
    assert slump(3.1, 2, 3.) == 2

def test_air():
    assert air(1, 2, 3.) == 1
    assert air(2, 2, 3.) == 0
    assert air(2.1, 2, 3.) == 0
    assert air(3, 2, 3.) == 0
    assert air(3.1, 2, 3.) == 2