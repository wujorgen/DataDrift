import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from BLUESKY.scrapers.bs4_scraper import scrape_data_payload
from BLUESKY.scrapers.genurls import gen_cars_com_urls
from BLUESKY.stats.clean import calc_pct_deltas, sort_trims

# // Let's make this function as a command line utility for now!
# Workflow is below.

# // Input yaml file as car dict.
# Format:
car_dict = {
    # "ford": ["mustang", "f_150"],
    "toyota": ["camry", "supra"],
    "bmw": [
        "330",
        "z4",
        "430",
        "m340",
        "m440",
    ],
    "audi": ["a4", "s4", "s3", "a5", "s5"]
    # "acura": ["integra"],
}

url_targets = gen_cars_com_urls(input_dict=car_dict)

# // SCRAPE SCRAPE SCRAPE
temp = scrape_data_payload(url_targets)

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
cat_model_list = []
for make in car_dict.keys():
    for model in car_dict[make]:
        filt = (df["make"] == make) & (df["model"] == model)
        scraped_results[make + "_" + model] = df[filt]

m340 = scraped_results["bmw_m340"]
m440 = scraped_results["bmw_m440"]
a4 = scraped_results["audi_a4"]
s3 = scraped_results["audi_s3"]
camry = scraped_results["toyota_camry"]

m440_mod = sort_trims(m440)
# a4 = sort_trims(a4)

m340 = calc_pct_deltas(m340)
m440 = calc_pct_deltas(m440)
a4 = calc_pct_deltas(a4)
s3 = calc_pct_deltas(s3)
camry = calc_pct_deltas(camry)

# // For each trim, perform sensitivity analysis.

# // Visualization!

# // Recommend best purchase point? Knee of the curve.

# // Ridge regression for price prediction?
