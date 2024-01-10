"""Defines an object to process the data in dataframes."""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

from DataDrift.stats import calc_pct_deltas, fit, exp_decay, estimate
from DataDrift import Drift

class DriftCar():
    def __init__(self, df:pd.DataFrame, source:str):
        if source=="carscom":
            """
            ['make', 'model', 'model_year', 'trim', 'mileage', 'price', 'listing_id','bodystyle']
            """
            self.make = self.try_to_load_one(df, "make")
            self.model = self.try_to_load_one(df, "model")

        else:
            print("Warning: you are trying to create a DriftCar for a source not yet enabled.")
    

    def try_to_load_one(self, df:pd.DataFrame, colname:str):
        """Tries to check and then load a column that should have a single value throughout.
        """
        try:
            temp = np.unique(df[f"{colname}"].values.tolist())
            if len(temp == 1):
                tempvar = temp[0]
            else:
                raise KeyError
        except KeyError:
            print(f"Key Error in Drift Car: {colname}")
            sys.exit(-20)
        except AttributeError:
            print(f"Attribute Error in Drift Car: {colname}")
            sys.exit(-21)
        return tempvar


def write_results(self, scraped_results, output_folder):
    """Saves plots and files of each car.
    Currently only tested to work with cars.com results.
    Args:
        scraped_results: just self.DATA_CARS for now
        output_folder: self.OUTPUTFOLDER
    Results:
    """
    for model in scraped_results.keys():
        print("======================")
        print(model)
        scraped_results[model].dropna(inplace=True)
        scraped_results[model] = calc_pct_deltas(scraped_results[model])

        xx = scraped_results[model]["mileage"].values.astype(float) / 1000

        # TODO: insert logic here that prints the trims to the screen
        # then prompts the user asking which one's they're interested in.

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
