import pandas as pd

def calc_pct_deltas(df:pd.DataFrame)->pd.DataFrame:
    df["year_delta"] = int(df["model_year"].max()) - df["model_year"].astype(int)
    df["price_pct"] = df["price"].astype(float) / float(df["price"].max()) - 1
    return df