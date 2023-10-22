import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.optimize import curve_fit


def exp_decay(x, A, B, C):
    """Models exponential decay with A*e^(-Bx)-C.

    Args:
        x: independant variable
        A: A
        B: B
        C: C

    Returns:
        dependant variable
    """
    return A * np.exp(-B * x) - C


def fit(
    df: pd.DataFrame,
    property: str = "mileage",
    func: str = "exp_decay",
    p0: list = [1, 1, 1],
):
    """Estimates vehicle price in relation to specified property.

    Args:
        asdf

    Returns:
        asdf
    """
    y = df["price_pct"]
    x = df[property].values.astype(float) / 1000

    if func=="exp_decay":
        popt, pcov = curve_fit(exp_decay, x, y, p0=p0)

    return popt, pcov


def estimate():
    pass