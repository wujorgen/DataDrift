# pytest looks for test_*.py or *_test.py

import numpy as np
from BLUESKY.scrapers import scraper

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def test_clean_number_NONE():
    scrap = scraper.CarSpider()
    assert scrap.get_clean_number("None") == "0"


def test_clean_number():
    scrap = scraper.CarSpider()
    assert scrap.get_clean_number('">2</') == "2"


def test_spider():
    spider = scraper.CarSpider
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(
        spider,
        start_urls=[
            "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true"
        ],
        debug_mode=True,
    )
    process.start()
    print(spider.data)


if __name__ == "__main__":
    test_spider()
