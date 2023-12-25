from DataDrift.scrapers.genurls import gen_zipcodes, gen_cars_com_urls


def test_zipcodes():
    assert gen_zipcodes(zarg=False) == [15238, 47907, 78701, 95814, 14623]


def test_url_generator():
    assert (
        gen_cars_com_urls({"Ford": ["Mustang"]}, [15238])[0]
        == "https://www.cars.com/shopping/results/?stock_type=all&makes=Ford&models=Ford-Mustang&zip=15238&maximum_distance=250&page_size=40&clean_title=true&no_accidents=true&personal_use=true"
    )
