import numpy as np
import pandas as pd
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
    target: str = "price_pct",
    func: str = "exp_decay",
) -> tuple:
    """Fits vehicle price function in relation to specified property.

    Args:
        df: dataframe containing price information
        property: what parameter to estimate depreciation off of
        target: target for estimation. price_pct OR price
        func: exp_decay OR not implemented
        p0: initial guesses for curve fitting

    Returns:
        tuple of coefficients, covariance OR -999 for error
    """
    if target not in ("price_pct", "price"):
        return -999
    y = df[target]
    x = df[property].values.astype(float)

    if func == "exp_decay":
        popt, pcov = curve_fit(exp_decay, x, y, p0=[y.max(), 1, 1])
    else:
        return -999

    return (popt, pcov)


def estimate(prop_value: float = 0, func: str = "exp_decay", p1: list = [0, 0, 0]):
    """Estimates vehicle price.

    Args:
        property: what parameter was used for fit
        prop_value: property value
        func: exp_decay OR not implemented
        p1: coefficients for function

    Returns:
        depreciation value. can be absolute price or percentage loss.
    """
    if func == "exp_decay":
        return exp_decay(prop_value, p1[0], p1[1], p1[2])
    else:
        return -999
