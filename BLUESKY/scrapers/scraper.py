import json
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher

import logging

logging.getLogger("scrapy").propagate = False


class CarSpider(scrapy.Spider):
    # https://www.edmunds.com/inventory/srp.html?inventorytype=used&make=toyota&model=gr-supra&trim=30-premium
    # https://www.edmunds.com/inventory/srp.html?inventorytype=used&make=bmw&model=3-series&trim=m340i
    # https://www.edmunds.com/inventory/srp.html?inventorytype=used&make=ford&model=mustang&trim=gt
    # https://www.edmunds.com/inventory/srp.html?inventorytype={TYPE}&make={MAKE}&model={MODEL}&trim={TRIM}

    # override constructor with custom settings - use start urls arg?

    # use callback function to collect the output of parse function
    # parse is called once per url so currently this overwrites the output text file with another url
    # see chatgpt - collect output
    # use the number of start_urls to create or list to record the json objects in -> class atribute
    # return this attribute to DB

    def __init__(self, name="CarSpider", start_urls=[], **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = start_urls
        # self.rawtext = []
        # self.payloads = []

    def parse(self, response):
        # txtfile = open("REEEEE.txt", "w") # for debugging
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
            data_dict["mileage"] = getCleanNumber(str(item.css("div.mileage").get()))
            data_dict["primary-price"] = getCleanNumber(
                str(item.css("span.primary-price").get())
            )

            yield data_dict


def getCleanNumber(input: str) -> str:
    if input == "None":
        return "0"
    else:
        return input[input.find('">') + 2 : input.find("</")]


def spider_results(start_urls=None, allowed_domains=None) -> list:
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
    process.crawl(CarSpider, start_urls=start_urls, allowed_domains=allowed_domains)
    process.start()  # the script will block here until the crawling is finished
    return results


if __name__ == "__main__":
    output = spider_results()
    for entry in output:
        print()
        print(entry)
