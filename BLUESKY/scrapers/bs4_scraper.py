import json
import re
from multiprocessing import Pool, cpu_count
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

    poolscraper = Pool(processes=int(cpu_count*0.69))
    margs = [[x] for x in urls]
    results = poolscraper.starmap(scrape_worker,margs)

    for ele in results:
        for dct in ele:
            list_out.append(dct)
    
    #for url in urls:
    #    list_out.append(scrape_worker(url))
    
    return list_out

def scrape_worker(url:str):
    """Worker function for scraping pool.
    
    Args:
        asdf

    Returns:
        asdf
    """
    list_out = []
    response = requests.get(url)
    # html_content = response.content
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all("div", class_="vehicle-details")
    links = soup.find_all("a", class_="sds-link")
    title = soup.title.text
    #if debug:
    #    list_out.append(title)
    #    continue
    for vehicle_div in divs:
        mileage_div = vehicle_div.find("div", class_="mileage")
        link_div = vehicle_div.find("a", class_="sds-link")
        if (link_div is not None) and (mileage_div is not None):
            data = link_div.get("data-override-payload")
            data_dict = json.loads(data)
            mileage = mileage_div.get_text()
            data_dict["mileage"] = re.sub(",", "", get_clean_number(mileage))
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
    breakpoint()
