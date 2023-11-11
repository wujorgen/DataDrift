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
        if type(spec) == str:
            return df[(df["trim"] == spec)]
        elif type(spec) == list:
            pass

    trims, counts = np.unique(np.array(df["trim"]), return_counts=True)
    lox = np.array(counts).argmax()

    trims2, counts2 = np.unique(np.array(df["bodystyle"]), return_counts=True)
    lox2 = np.array(counts).argmax()

    if opt == "popular":
        return df[(df["trim"] == trims[lox])]
    else:
        return df


def process_data_payload(temp: list[dict], car_dict: dict):
    """Process the results from scrap_data_payload from cars.com.

    Args:
        temp: result of scrape_data_payload
        car_dict: dictionary of all car models targeted for scraping

    Returns:
        dict of dataframes. each data frame contains information on a make_model
    """
    columns = [
        "make",
        "model",
        "model_year",
        "trim",
        "mileage",
        "price",
        "listing_id",
        "bodystyle",
    ]
    df = pd.DataFrame(temp, columns=columns)
    scraped_results = {}
    for make in car_dict.keys():
        for model in car_dict[make]:
            filt = (df["make"] == make) & (df["model"] == model)
            scraped_results[make + "_" + model] = df[filt]
    return scraped_results


def calc_pct_deltas(df: pd.DataFrame) -> pd.DataFrame:
    """Adds percent change metrics to data frame.

    Args:
        df: preprocessed dataframe of one model and/or trim containing car listings

    Returns:
        df: original dataframe with metrics added.
    """
    df["year_delta"] = int(df["model_year"].max()) - df["model_year"].astype(int)
    df["price_pct"] = df["price"].astype(float) / float(df["price"].max()) - 1
    return df
