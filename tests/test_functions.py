# pytest looks for test_*.py or *_test.py

import numpy as np
from BLUESKY.scrapers import scraper


def test_CleanNumber_NONE():
    scrap = scraper.CarSpider()
    assert scrap.getCleanNumber("None") == "0"
