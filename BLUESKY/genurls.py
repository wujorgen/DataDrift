def gen_urls(ZIPS: list, MAKES: list, MODELS: list, site: str = "None") -> list:
    urls = []
    if site == "None":
        return ["WARNING!", "NO SITES DEFINED!"]
    elif site == "AUTOTRADER":
        for aZIP, bMAKE, cMODEL in zip(ZIPS, MAKES, MODELS):
            urls.append(
                f"https://www.autotrader.com/cars-for-sale/all-cars?zip={aZIP}&makeCodeList={bMAKE}&modelCodeList={cMODEL}"
            )
    else:
        return [
            "WARNING!",
            "THE SCRAPER HAS NOT BEEN CONFIGURED TO HANDLE THE SITE YOU HAVE REQUESTED!",
        ]
    return urls


def genAutoTempestURLS(
    ZIPS: list, MAKES: list, MODELS: list, TRIMS: list, site: str = "None"
) -> list:
    urls = []

    return urls


def genCarsComURLS(
    ZIPS: list, MAKES: list, MODELS: list, TRIMS: list, site: str = "None"
) -> list:
    urls = []
    """
    https://www.cars.com/shopping/results/?
    dealer_id=
    &keyword=
    &list_price_max=
    &list_price_min=
    &makes[]=ford
    &maximum_distance=20
    &mileage_max=
    &models[]=ford-mustang
    &monthly_payment=
    &page_size=20
    &sort=best_match_desc
    &stock_type=used
    &trims[]=ford-mustang-gt
    &year_max=
    &year_min=
    &zip=15238
    &clean_title=true
    &no_accidents=true
    &personal_use=true
    """

    """
    https://www.cars.com/shopping/results/?
    stock_type=all
    &makes=toyota (bmw)
    &models=toyota-supra (bmw-m340)
    &list_price_max=
    &maximum_distance=30
    &zip=15238
    """

    """https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=30&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true"""

    return urls
