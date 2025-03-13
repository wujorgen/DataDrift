import json
import re
from multiprocessing import Pool, cpu_count

import pandas as pd
import requests
from bs4 import BeautifulSoup


def process_carscom(temp: list[dict], car_dict: dict):
    """Process the results from scrap_carscom from cars.com.

    Args:
        temp: result of scrape_carscom
        car_dict: dictionary of all car models targeted for scraping

    Returns:
        dict of dataframes. each data frame contains information on a make_model
    """
    columns = [
        "make",
        "model",
        "model_year",
        "trim",
        "mileage",
        "price",
        "listing_id",
        "bodystyle",
    ]
    df = pd.DataFrame(temp, columns=columns)
    scraped_results = {}
    for make in car_dict.keys():
        for model in car_dict[make]:
            filt = (df["make"] == make) & (df["model"] == model)
            scraped_results[make + "_" + model] = df[filt]
    return scraped_results


def scrape_carscom(urls: list[str], debug=False) -> list[dict]:
    """Scrapes a cars dot com url for the data override payload attribute.

    Args:
        urls: list of strings where each string is url.

    Returns:
        list: list of dicts containing data.
    """
    list_out = []

    if debug:
        for url in urls:
            list_out.append(scrape_worker(url, debug=True))
            print(list_out)
        return list_out

    poolscraper = Pool(processes=int(cpu_count() * 0.69))
    margs = [[x] for x in urls]
    results = poolscraper.starmap(scrape_worker, margs)

    for ele in results:
        for dct in ele:
            list_out.append(dct)

    # for url in urls:
    #    list_out.append(scrape_worker(url))

    return list_out


def scrape_worker(url: str, debug=False) -> list:
    """Worker function for scraping pool.

    Args:
        url: string containing target URL to a cars.com search.

    Returns:
        list_out: list of dicts, where each dict is a data payload.
    """
    list_out = []
    response = requests.get(url)
    # html_content = response.content
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all("div", class_="vehicle-details")
    links = soup.find_all("a", class_="sds-link")  # noqa F841
    title = soup.title.text
    if debug: 
        return title
    for vehicle_div in divs:
        mileage_div = vehicle_div.find("div", class_="mileage")
        link_div = vehicle_div.find("a", class_="sds-link")
        if (link_div is not None) and (mileage_div is not None):
            data = link_div.get("data-override-payload")
            data_dict = json.loads(data)
            mileage = mileage_div.get_text()
            data_dict["mileage"] = re.sub(",", "", re.sub("mi.", "", mileage))
            list_out.append(data_dict)
    return list_out


# if __name__ == "__main__":
#    start_urls = [
#        "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true",
#        "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=toyota&models=toyota-supra&clean_title=true&no_accidents=true&personal_use=true",
#    ]
#    temp = scrape_data_payload(start_urls)
#    print(temp)
#    print("SOUP TIME")
#    breakpoint()
#
