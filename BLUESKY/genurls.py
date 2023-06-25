"""Let's generate some URLS!
start_urls = [
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true",
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=toyota&models=toyota-supra&clean_title=true&no_accidents=true&personal_use=true",
]
"""


def gen_cars_com_urls(
    makes: list,
    models: list,
    trims: list or bool = False,
    zipcodes: list or bool = False,
) -> list:
    """Generates urls for Cars.com.
    
        Args:
            makes:
            models:
            trims (optional):
            zipcodes (optional):

        Returns:
            list of all generated urls
    """
    """
    https://www.cars.com/shopping/results/?
    dealer_id=
    &keyword=
    &list_price_max=
    &list_price_min=
    -> &makes[]=ford toyota (bmw)
    -> &maximum_distance=250
    &mileage_max=
    -> &models[]=ford-mustang toyota-supra (bmw-m340)
    &monthly_payment=
    -> &page_size=40
    &sort=best_match_desc
    -> &stock_type=used all
    -> &trims[]=ford-mustang-gt
    &year_max=
    &year_min=
    -> &zip=15238
    -> &clean_title=true
    -> &no_accidents=true
    -> &personal_use=true
    """
    urls = []
    for idx in range(len(models)):
        for zcode in usa_metro_zipcodes():
            #print(idx, makes[idx], models[idx], zcode)
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


def usa_metro_zipcodes():
    """Hardcoded function to return zipcodes to all major USA metropolitan areas."""
    # TODO
    return [15238, 47907]


if __name__ == "__main__":
    temp = gen_cars_com_urls(makes=["ford", "toyota"], models=["mustang", "supra"])
    for each in temp: 
        print(each)