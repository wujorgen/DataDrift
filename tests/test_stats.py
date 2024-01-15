from DataDrift.stats import  calc_pct_deltas, sort_trims, estimate, exp_decay, fit 

import numpy as np

def test_estimate_999():
    assert estimate(0, "wrong input") == -999

def test_fit():
    pass

def test_exp_decay_fit():
    """ A * np.exp(-B * x) - C <- (x,A,B,C)"""
    assert exp_decay(1,1,1,1) == np.exp(-1) - 1
    assert exp_decay(-1,-1,-1,-1) == -1 * np.exp(-1) + 1

def test_calc_pct_deltas():
    pass