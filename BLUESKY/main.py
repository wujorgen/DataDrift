import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from BLUESKY.scrapers.bs4_scraper import scrape_data_payload
from BLUESKY.scrapers.genurls import gen_cars_com_urls
from BLUESKY.stats.clean import calc_pct_deltas, sort_trims, process_data_payload
from BLUESKY.stats.sensitivity import fit, estimate, exp_decay

# // Let's make this function as a command line utility for now!
# Workflow is below.


if __name__ == "__main__":
    output_folder = "BLUESKY_OUTPUT"
    if not os.path.isdir(os.path.join(os.getcwd(), output_folder)):
        os.mkdir(os.path.join(os.getcwd(), output_folder))
    # // Input yaml file as car dict.
    # Format:
    car_dict = {
        #"ford": ["mustang"],
        "chevrolet": ["camaro"],
        #"toyota": ["camry", "supra"],
        #"bmw": ["z4", "m340", "m440"],
        #"audi": ["rs_3", "s3", "rs_5", "s5"],
        "porsche": ["718_cayman", "718_boxster"],
        "lexus": ["rc_f"],
    }
    url_targets = gen_cars_com_urls(input_dict=car_dict)

    # // SCRAPE SCRAPE SCRAPE
    temp = scrape_data_payload(url_targets)

    scraped_results = process_data_payload(temp=temp, car_dict=car_dict)

    print(scraped_results.keys())

    # // For each model, do stuff.
    # TODO: make this consider trims too.
    # TODO: make this a function and multiprocess it lol. pool after splitting by keys to avoid race condition?
    for model in scraped_results.keys():
        print("======================")
        print(model)
        scraped_results[model].dropna(inplace=True)
        scraped_results[model] = calc_pct_deltas(scraped_results[model])

        xx = scraped_results[model]["mileage"].values.astype(float) / 1000

        try:
            pct_opt, pct_cov = fit(
                df=scraped_results[model],
                target="price_pct",
                property="mileage",
                func="exp_decay",
            )
            print(pct_opt)
            plt.figure()
            plt.scatter(
                xx,
                scraped_results[model]["price_pct"],
            )
            pct_fit = exp_decay(
                xx,
                pct_opt[0],
                pct_opt[1],
                pct_opt[2],
            )

            tempdf = pd.DataFrame([xx, pct_fit])
            tempdf = tempdf.T.sort_values(0)
            plt.plot(tempdf[0], tempdf[1], c="red")
            plt.xlabel("miles (1000s)")
            plt.ylabel("depreciation")
            plt.title(f"{model} depreciation")
            plt.savefig(f"{output_folder}/{model}_depreciation")
            plt.close()
        except RuntimeError as e:
            print(f"Runtime error encountered for {model}. See below:")
            print(e)
            breakpoint()
            continue
        try:
            p_opt, p_cov = fit(
                df=scraped_results[model],
                target="price",
                property="mileage",
                func="exp_decay",
            )
            print(p_opt)
            plt.figure()
            plt.scatter(
                xx,
                scraped_results[model]["price"],
            )
            p_fit = exp_decay(
                xx,
                p_opt[0],
                p_opt[1],
                p_opt[2],
            )
            tempdf = pd.DataFrame([xx, p_fit])
            tempdf = tempdf.T.sort_values(0)
            plt.plot(tempdf[0], tempdf[1], c="red")
            plt.xlabel("miles (1000s)")
            plt.ylabel("price")
            plt.title(f"{model} price")
            plt.savefig(f"{output_folder}/{model}_price")
            plt.close()
        except RuntimeError as e:
            print(f"Runtime error encountered for {model}. See below:")
            print(e)
            breakpoint()
            continue

    # // Recommend best purchase point? Knee of the curve.
    breakpoint()
