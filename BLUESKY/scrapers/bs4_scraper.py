import json
import re

import requests
from bs4 import BeautifulSoup


def scrape_data_payload(urls: list[str], debug=False) -> list[dict]: # TODO: use mp pool to speed this up
    """Scrapes a cars dot com url for the data override payload attribute.

    Args:
        urls: list of strings where each string is url.

    Returns:
        list: list of dicts containing data.
    """
    list_out = []
    # print(urls[0])
    for url in urls:
        response = requests.get(url)
        # html_content = response.content
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.find_all("div", class_="vehicle-details")
        links = soup.find_all("a", class_="sds-link")
        title = soup.title.text
        # print(title)
        if debug:
            list_out.append(title)
            continue
        # print(title)
        for vehicle_div in divs:
            mileage_div = vehicle_div.find("div", class_="mileage")
            link_div = vehicle_div.find("a", class_="sds-link")
            # print("=====")
            if (link_div is not None) and (mileage_div is not None):
                data = link_div.get("data-override-payload")
                data_dict = json.loads(data)
                mileage = mileage_div.get_text()
                data_dict["mileage"] = re.sub(",", "", get_clean_number(mileage))
                # print(data_dict)
                list_out.append(data_dict)
    return list_out


def get_clean_number(input: str) -> str:
    if input == "None":
        return "0"
    else:
        return input[input.find('">') + 1 : input.find("</") - 3]


if __name__ == "__main__":
    start_urls = [
        "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true",
        "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=toyota&models=toyota-supra&clean_title=true&no_accidents=true&personal_use=true",
    ]
    temp = scrape_data_payload(start_urls)
    print(temp)
    print("SOUP TIME")
