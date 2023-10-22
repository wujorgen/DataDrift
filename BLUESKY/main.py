from BLUESKY.scrapers.bs4_scraper import scrape_data_payload
from BLUESKY.scrapers.genurls import gen_cars_com_urls
from BLUESKY.stats import clean
from BLUESKY.stats import sensitivity

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#// Let's make this function as a command line utility for now!
# Workflow is below.

#// Input yaml file as car dict. 
# Format:
'''
car_dict = {
    "ford": ["mustang", "f_150"],
    "toyota": ["camry", "supra"],
    "bmw": ["330", "z4", "430", "m340", "m440",],
    "acura": ["integra"],
}

url_targets = gen_cars_com_urls(input_dict=car_dict)
'''

#// SCRAPE SCRAPE SCRAPE
# temp = scrape_data_payload(url_targets)

#// Fetch list of car models, then trims per model. 

#// For each make/model/trim, prompt user for analysis options. 
# Default option is to perform analysis only for most popular trim.

#// Clean & preprocess dataframes using this code sample:
'''
m440["year_delta"] = int(m440["model_year"].max()) - m440["model_year"].astype(int)
m440["price_pct"] = m440["price"].astype(float) / float(m440["price"].max()) - 1
'''

#// For each trim, perform sensitivity analysis.

#// Visualization!

#// Recommend best purchase point? Knee of the curve.