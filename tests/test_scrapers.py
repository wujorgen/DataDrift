# pytest looks for test_*.py or *_test.py

import numpy as np
from DataDrift.scrapers.carscom import scrape_carscom, get_clean_number


def test_payload_debug():
    start_urls = [
        "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true",
        "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=toyota&models=toyota-supra&clean_title=true&no_accidents=true&personal_use=true",
    ]
    url_titles = scrape_carscom(start_urls, debug=True)
    if "Ford Mustang" in url_titles[0]:
        print("MORD FUSTANG")
    if "Toyota Supra" in url_titles[1]:
        print("ITS A BMW")
    assert "Ford Mustang" in url_titles[0]
    assert "Toyota Supra" in url_titles[1]


def test_get_clean_number():
    assert True
