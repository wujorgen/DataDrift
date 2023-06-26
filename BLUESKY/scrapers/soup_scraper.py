from bs4 import BeautifulSoup
import requests
import json

def scrape_data_payload(urls:list[str])->list[dict]:
    """Scrapes a cars dot com url for the data override payload attribute.

        Args:
            urls: list of strings where each string is url.

        Returns:
            list: list of dicts containing data.
    """
    print(urls[0])
    response = requests.get(urls[0])
    html_content = response.content
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all("div", class_="vehicle-details")
    links = soup.find_all("a", class_="sds-link")
    title = soup.title.text
    print(title)

    for vehicle_div in divs:
        mileage_div = vehicle_div.find('div', class_='mileage')
        link_div = vehicle_div.find("a", class_="sds-link")
        print("=====")
        if (link_div is not None) and (mileage_div is not None):
            data = link_div.get("data-override-payload")
            data_dict = json.loads(data)
            print(data_dict)
            mileage = mileage_div.get_text()
            print(mileage, get_clean_number(mileage)) #TODO: replace the comma with nothing




    #for link in links:
    #    print()
    #    data = link.get("data-override-payload")
    #    if data is not None:
    #        data_dict = json.loads(link.get("data-override-payload"))
    #        print(data_dict)


    #with open("carsoutfile.txt", "w") as outfile:
    #    for ele in soup.contents:
    #        outfile.write(str(ele))
    #with open("linkdump.txt", "w") as pp:
    #    for div in divs:
    #        pp.write(str(div))
    #        pp.write("\nASDFGHJKL\n")

def get_clean_number(input: str) -> str:
        if input == "None":
            return "0"
        else:
            return input[input.find('">') + 1 : input.find("</")-3]

if __name__=="__main__":
    start_urls = [
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true",
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=toyota&models=toyota-supra&clean_title=true&no_accidents=true&personal_use=true",
    ]
    scrape_data_payload(start_urls)
    print("SOUP TIME")