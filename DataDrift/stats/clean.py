import numpy as np
import pandas as pd


# TODO: this needs work to "intelligently" parse trims
def sort_trims(df: pd.DataFrame, opt: str = "popular", spec: str = "") -> pd.DataFrame:
    """Cleans trims of dataframe. NOT PRODUCTION READY

    Args:
        df: preprocessed dataframe of one model and/or trim containing car listings
        opt: default is "popular", "spec" to specify trim
        spec: default is blank. use to specify a trim if you want. overrides opt.

    Returns:
        df: cleaned dataframe
    """
    if spec != "":
        if type(spec) is str:
            return df[(df["trim"] == spec)]
        elif type(spec) is list:
            pass

    trims, counts = np.unique(np.array(df["trim"]), return_counts=True)
    lox = np.array(counts).argmax()

    trims2, counts2 = np.unique(
        np.array(df["bodystyle"]), return_counts=True
    )  # noqa F401
    lox2 = np.array(counts).argmax()  # noqa F401

    if opt == "popular":
        return df[(df["trim"] == trims[lox])]
    else:
        return df


def calc_pct_deltas(df: pd.DataFrame) -> pd.DataFrame:
    """Adds percent change metrics to data frame.

    Args:
        df: preprocessed dataframe of one model and/or trim containing car listings

    Returns:
        df: original dataframe with metrics added.
    """
    max_model_year = int(df["model_year"].max())
    max_price = float(df["price"].max())

    # Use "copy" to avoid some dumb slicing warning
    df = df.copy()

    df["year_delta"] = max_model_year - df["model_year"].astype(int)
    df["price_pct"] = df["price"].astype(float) / max_price - 1
    return df
