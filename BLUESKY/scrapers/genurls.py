"""Let's generate some URLS!"""

import pandas as pd


def gen_cars_com_urls(
    makes: list,
    models: list,
    trims: list or bool = False,
    zarg: list or bool = False,
) -> list:
    """Generates urls for Cars.com.

    Args:
        makes:
        models:
        trims (optional):
        zarg (optional):

    Returns:
        list of all generated urls
    """
    """
    https://www.cars.com/shopping/results/?
    dealer_id=
    &keyword=
    &list_price_max=
    &list_price_min=
    -> &makes=ford toyota (bmw)
    -> &maximum_distance=250
    &mileage_max=
    -> &models=ford-mustang toyota-supra (bmw-m340)
    &monthly_payment=
    -> &page_size=40
    &sort=best_match_desc
    -> &stock_type=used all
    -> &trims=ford-mustang-gt
    &year_max=
    &year_min=
    -> &zip=15238
    -> &clean_title=true
    -> &no_accidents=true
    -> &personal_use=true
    """
    urls = []
    for idx in range(len(models)):
        for zcode in gen_zipcodes(zarg):
            # print(idx, makes[idx], models[idx], zcode)
            urls.append(
                "https://www.cars.com/shopping/results/?"
                + "stock_type=all"
                + "&makes="
                + makes[idx]
                + "&models="
                + makes[idx]
                + "-"
                + models[idx]
                + "&zip="
                + str(zcode)
                + "&maximum_distance=250"
                + "&page_size=40"
                + "&clean_title=true"
                + "&no_accidents=true"
                + "&personal_use=true"
            )
    return urls


def gen_zipcodes(zarg: bool = False or list[int]) -> list[int]:
    """Haven't finished this yet.

    Args:
        zarg: False is default, True is auto gen metro list. Not sure what to do with the list.
    """
    df = pd.read_html("https://vanwilson.info/2014/11/sample-zip-codes-50-states/")[0]
    # print(df)
    if zarg:
        return df["Representative ZIP Code"].to_list()
    elif type(zarg) == list[int]:
        return [0]
    else:
        return [15238, 47907, 78701, 95814]
