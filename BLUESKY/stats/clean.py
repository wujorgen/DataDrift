import pandas as pd
import numpy as np

#TODO: this needs work to "intelligently" parse trims
def sort_trims(df:pd.DataFrame, opt:str="popular")->pd.DataFrame:
    """Cleans trims of dataframe.

    Args:
        df: preprocessed dataframe of one model and/or trim containing car listings
        opt: default "popular"|"", 

    Returns:
        df: cleaned dataframe
    """
    trims, counts = np.unique(np.array(df["trim"]),return_counts=True)
    lox = np.array(counts).argmax()

    trims2, counts2 = np.unique(np.array(df["bodystyle"]),return_counts=True)
    lox2 = np.array(counts).argmax()

    if opt=="popular":
        return df[(df["trim"]==trims[lox])]
    else: 
        return df

def calc_pct_deltas(df:pd.DataFrame)->pd.DataFrame:
    """Adds percent change metrics to data frame.

    Args:
        df: preprocessed dataframe of one model and/or trim containing car listings

    Returns:
        df: original dataframe with metrics added.
    """
    df["year_delta"] = int(df["model_year"].max()) - df["model_year"].astype(int)
    df["price_pct"] = df["price"].astype(float) / float(df["price"].max()) - 1
    return df