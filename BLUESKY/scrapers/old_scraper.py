'''DEFUNCT
import json
import logging

import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

logging.getLogger("scrapy").propagate = False


class CarSpider(scrapy.Spider):
    def __init__(self, name="CarSpider", start_urls=[], debug_mode = False, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = start_urls
        self.debug_mode = debug_mode

    def parse(self, response):
        txtfile = open("REEEEE.txt", "w") # for debugging
        print(response.css("h1::text").get())
        for item in response.css(
            "div.vehicle-details"
        ):  # iterates over scrapy selectors
            # txtfile.write("\n\n--- NEW DIV ---\n\n")
            # txtfile.write(item.css("div").get())
            # print(str(item.css('h2::text').get()))
            # print('|_ ' + getCleanNumber(str(item.css('span.primary-price').get())))
            # print('|_ ' + getCleanNumber(str(item.css('div.mileage').get())))
            # there is a payload that appears to only be included for used cars?
            # for the purpose of visualizing depreciation surface, it might be better to not pull new data
            # print("\nNEW ENTRY")
            payload = item.css(
                "a[data-override-payload]::attr(data-override-payload)"
            ).get()
            data_dict = json.loads(payload)
            data_dict["mileage"] = self.get_clean_number(
                str(item.css("div.mileage").get())
            )
            data_dict["primary-price"] = self.get_clean_number(
                str(item.css("span.primary-price").get())
            )

            yield data_dict


    def get_clean_number(self, input: str) -> str:
        if input == "None":
            return "0"
        else:
            return input[input.find('">') + 2 : input.find("</")]


def get_spider_results(start_urls=None, allowed_domains=None) -> list:
    if start_urls == None:
        start_urls = [
            "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true",
            "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=toyota&models=toyota-supra&clean_title=true&no_accidents=true&personal_use=true",
        ]
    if allowed_domains == None:
        allowed_domains = ["cars.com"]

    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    process.crawl(CarSpider, start_urls=start_urls, allowed_domains=allowed_domains, debug_mode=True)
    process.start()  # the script will block here until the crawling is finished
    return results


if __name__ == "__main__":
    output = get_spider_results()
    for entry in output:
        print()
        print(entry)
'''