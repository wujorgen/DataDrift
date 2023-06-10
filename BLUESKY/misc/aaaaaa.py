from bs4 import BeautifulSoup
import requests


response = requests.get(
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=30&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true"
)


soup = BeautifulSoup(response.text, "html.parser")

title = soup.title.text
print(title)

print(type(soup.contents))


with open("carsoutfile.txt", "w") as outfile:
    for ele in soup.contents:
        outfile.write(str(ele))
