from DataDrift.scrapers.genurls import gen_zipcodes, gen_carscom_urls


def test_zipcodes():
    assert gen_zipcodes(zarg=False) == [15238, 47907, 78701, 95814, 14623]
    assert gen_zipcodes(zarg=True) == [
        36104,
        99801,
        85001,
        72201,
        95814,
        80202,
        6103,
        19901,
        32301,
        30303,
        96813,
        83702,
        62701,
        46225,
        50309,
        66603,
        40601,
        70802,
        4330,
        21401,
        2201,
        48933,
        55102,
        39205,
        65101,
        59623,
        68502,
        89701,
        3301,
        8608,
        87501,
        12207,
        27601,
        58501,
        43215,
        73102,
        97301,
        17101,
        2903,
        29217,
        57501,
        37219,
        78701,
        84111,
        5602,
        23219,
        98507,
        25301,
        53703,
        82001,
        96799,
        20001,
        96941,
        96910,
        96960,
        96950,
        96939,
        901,
        802,
    ]


def test_url_generator():
    assert (
        gen_carscom_urls({"Ford": ["Mustang"]}, [15238])[0]
        == "https://www.cars.com/shopping/results/?stock_type=all&makes=Ford&models=Ford-Mustang&zip=15238&maximum_distance=250&page_size=40&clean_title=true&no_accidents=true&personal_use=true"
    )
