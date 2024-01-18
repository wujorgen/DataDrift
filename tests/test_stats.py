from DataDrift.stats import  calc_pct_deltas, sort_trims, estimate, exp_decay, fit 

import numpy as np
import pandas as pd

def test_estimate():
    assert estimate(0, "wrong input") == -999
    assert round(estimate(1, "exp_decay", [1,1,1]),5) == -0.63212

def test_fit():
    x = {"A":[1,2,3,4], "price":[10,6,4,2], "price_pct":[6,3,2,1]}
    xx = pd.DataFrame(x)
    assert fit(df=xx, property="A", target="wtf", func="exp_decay") == -999
    assert fit(df=xx, property="A", target="price_pct", func="wtf") == -999

def test_exp_decay():
    """ A * np.exp(-B * x) - C <- (x,A,B,C)"""
    assert exp_decay(1,1,1,1) == np.exp(-1) - 1
    assert exp_decay(-1,-1,-1,-1) == -1 * np.exp(-1) + 1

def test_calc_pct_deltas():
    dfx = {"model_year":[2022,2023],"price":[30000,35000]}
    df = pd.DataFrame(dfx)
    df_answer = pd.DataFrame({"model_year":[2022,2023],"price":[30000,35000],"year_delta":[1,0],"price_pct":[-0.142857,0.0]})
    df_calc = calc_pct_deltas(df)
    pd.testing.assert_frame_equal(df_calc, df_answer, check_dtype=False)
