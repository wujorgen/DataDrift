import numpy as np
from scipy.optimize import curve_fit


def exponential_decay(x, a, b, c):
    """Exponential model: y = a * exp(-b * x) + c"""
    return a * np.exp(-b * x) + c


def fit_exponential_curve(df, x_col="miles", y_col="price"):
    """
    Fits exponential decay parameters (a, b, c) and generates smooth
    curve points for plotting.
    """
    if len(df) < 3:
        return None  # Need at least 3 points to fit 3 parameters

    x_data = df[x_col].values
    y_data = df[y_col].values

    # Initial guesses: A ~ price range, b ~ small decay factor, C ~ min price
    initial_guess = (y_data.max() - y_data.min(), 0.00003, y_data.min())

    try:
        # Fit curve using non-linear least squares
        popt, _ = curve_fit(
            exponential_decay,
            x_data,
            y_data,
            p0=initial_guess,
            bounds=(0, [np.inf, 1.0, np.inf]),
            maxfev=5000,
        )

        # Generate smooth X values for drawing the line
        x_smooth = np.linspace(x_data.min(), x_data.max(), 100)
        y_smooth = exponential_decay(x_smooth, *popt)

        return x_smooth, y_smooth, popt
    except Exception as e:
        # Returns None if optimization fails to converge
        return None
