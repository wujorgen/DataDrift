# pytest looks for test_*.py or *_test.py

from BLUESKY.scrapers import scraper


def test_CleanNumber_NONE():
    assert scraper.getCleanNumber("None") == "0"
