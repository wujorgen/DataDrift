from BLUESKY.genurls import gen_zipcodes, gen_cars_com_urls


def test_zipcodes():
    assert gen_zipcodes(zarg=False) == [15238, 47907]

def test_url_generator():
    print(gen_cars_com_urls(["Ford"],["Mustang"]))
