from BLUESKY.genurls import usa_metro_zipcodes


def test_zipcodes():
    assert usa_metro_zipcodes() == [15238, 47907]
