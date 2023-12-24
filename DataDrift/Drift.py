"""Defines the Drift class."""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from DataDrift.scrapers.cars_scraper import scrape_data_payload
from DataDrift.scrapers.genurls import gen_cars_com_urls
from DataDrift.stats.clean import calc_pct_deltas, process_data_payload, sort_trims
from DataDrift.stats.sensitivity import estimate, exp_decay, fit


class Drift:
    def __init__(self, path_in: str or bool = None, dict_in=None):
        """Initializes the Drift class.

        Args:
            path_in: Path to input yaml. Default. If not specified, looks in current directory.
            dict_in: Dict of inputs. Optional, overrides path_in. Format is {"car": ["model"]}
        """
        self.ROOTFOLDER = os.getcwd()
        self.OUTPUTFOLDER = os.path.join(self.ROOTFOLDER, "DataDriftOutput")
        if not os.path.isdir(self.OUTPUTFOLDER):
            os.mkdir(self.OUTPUTFOLDER)
        if not path_in:
            self.INPUTFILE = os.path.join(self.ROOTFOLDER, "DataDrift.yaml")
        else:
            self.INPUTFILE = path_in
        if dict_in is None:
            if os.path.exists(self.INPUTFILE):
                with open(self.INPUTFILE, "r") as input_doc:
                    try:
                        self.CARDICT = yaml.safe_load(input_doc)
                    except yaml.YAMLError:
                        print("ERROR IN INPUT DECK.")
                        sys.exit(-1)
            else:
                print("Oops there's no input file.")
                sys.exit()
        else:
            self.CARDICT = dict_in
        # Time to scrape!
        # logic needs to be added to handle scraping from multiple websites
        self.DATA_CARS = self.scrape_cars(self.CARDICT)
        self.write_results(self.DATA_CARS, self.OUTPUTFOLDER)
        breakpoint()

    def scrape_cars(self, car_dict) -> dict:
        """Scrapes results from cars.com.
        Args:
            car_dict:
        """
        url_targets = gen_cars_com_urls(input_dict=self.CARDICT)
        temp = scrape_data_payload(url_targets)
        results = process_data_payload(temp=temp, car_dict=car_dict)
        # print(self.RESULTS.keys())
        return results

    def scrape_edmunds(self, car_dict) -> dict:
        """Scrapes results from edmunds.com.
        Args:
            car_dict:
        """
        # TODO
        pass

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
