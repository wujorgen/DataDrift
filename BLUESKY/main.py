import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from BLUESKY.scrapers.bs4_scraper import scrape_data_payload
from BLUESKY.scrapers.genurls import gen_cars_com_urls
from BLUESKY.stats.clean import calc_pct_deltas, sort_trims, process_data_payload
from BLUESKY.stats.sensitivity import fit, estimate

# // Let's make this function as a command line utility for now!
# Workflow is below.

# // Input yaml file as car dict.
# Format:
car_dict = {
    "ford": ["mustang"],
    "chevrolet": ["camaro"],
    "toyota": ["camry", "supra"],
    "bmw": ["z4", "m340", "m440"],
    "audi": ["a4", "s4", "s3", "a5", "s5"],
    "porsche": ["718_cayman", "718_boxster"],
    "lexus": ["rc_f"],
}

url_targets = gen_cars_com_urls(input_dict=car_dict)

# // SCRAPE SCRAPE SCRAPE
temp = scrape_data_payload(url_targets)

scraped_results = process_data_payload(temp=temp, car_dict=car_dict)

print(scraped_results.keys())

# // For each model, do stuff. TODO: make this consider trims too.
for model in scraped_results.keys():
    print(model)
    scraped_results[model].dropna(inplace=True)
    scraped_results[model] = calc_pct_deltas(scraped_results[model])
    popt, pcov = fit(
        df=scraped_results[model], property="mileage", func="exp_decay", p0=[1, 1, 1]
    )


# // Recommend best purchase point? Knee of the curve.
