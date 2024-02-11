"""Defines DriftCar, an object to store individual car data."""
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from DataDrift.stats import calc_pct_deltas, estimate, exp_decay, fit  # noqa F401


class DriftCar:
    """This class houses the data for each car, and writing and processing methods."""

    def __init__(self, df: pd.DataFrame, source: str, lookback: int = 12):
        """Constructor for drift car.

        Args:
            df: car info dataframe
            source: website the info was scraped from
            lookback: number of years to include in function fit. default is 12.

        """
        self.make = self._try_to_load_one_(df, "make")
        self.model = self._try_to_load_one_(df, "model")
        self.data = df.dropna().drop_duplicates()

        if source == "carscom":
            """
            ['make', 'model', 'model_year', 'trim', 'mileage', 'price', 'listing_id','bodystyle']  # noqa E501
            """
            self.data = calc_pct_deltas(self.data)
            self.source = "carscom"
            self.data["url"] = "cars.com/vehicledetail/" + self.data["listing_id"]

        else:
            print("Warning: Source not yet enabled for DriftCar.")

        self.data["grand_mileage"] = self.data["mileage"].astype(float) / 1000.0
        self.fit_data = self.data[(self.data["year_delta"] <= lookback)]
        self.fit_type = "exp_decay"
        self.pct_opt, self.pct_cov = fit(
            df=self.fit_data,
            target="price_pct",
            property="grand_mileage",
            func=self.fit_type,
        )
        self.p_opt, self.p_cov = fit(
            df=self.fit_data,
            target="price",
            property="grand_mileage",
            func=self.fit_type,
        )
        self.data["predicted_price"] = exp_decay(
            self.data["grand_mileage"].values.astype(float),
            self.p_opt[0],
            self.p_opt[1],
            self.p_opt[2],
        )

    def _try_to_load_one_(self, df: pd.DataFrame, colname: str):
        """INTERNAL: Tries to check and then load a column that should have a single value throughout."""  # noqa E501
        try:
            temp = np.unique(df[colname].values.tolist())
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

    def writeall(self, fpath: str):
        """Writes all info: plots, function fits, and raw csvs.

        Args:
            fpath: desired output folder, must exist.
        """
        self.writecsv(fpath)
        self.writeplots(fpath)
        self.writefunction(fpath)

    def writecsv(self, fpath: str):
        """Writes data to output files.

        Args:
            fpath: desired output folder, must exist.
        """
        self.data.to_csv(fpath + f"/{self.make}_{self.model}.csv")

    def writeplots(self, fpath: str):
        """Writes plots for easy visualization.

        Args:
            fpath: desired output folder, must already exist.
        """
        plt.figure()
        plt.scatter(
            self.data["grand_mileage"],
            self.data["price"],
        )
        tempdf = pd.DataFrame(
            [self.data["grand_mileage"], self.data["predicted_price"]]
        ).T
        tempdf.sort_values("grand_mileage", inplace=True)
        plt.plot(
            tempdf["grand_mileage"], tempdf["predicted_price"], c="red"
        )  # fix this to use a local sorted copy
        plt.xlabel("miles (1000s)")
        plt.ylabel("price")
        plt.xlim((0, 120))
        plt.grid()
        plt.title(f"{self.make} {self.model} price")
        plt.savefig(fpath + f"/{self.make}_{self.model}_price")
        plt.close()

    def writefunction(self, fpath: str):
        """Writes function fit for later consideration.

        Args:
            fpath: desired output folder, must already exist.
        """
        with open(f"{fpath}/{self.make}_{self.model}_function.txt", "w") as file:
            if self.fit_type == "exp_decay":
                """A * np.exp(-B * x) - C : popt = A,B,C"""
                file.write("Function: A * np.exp(-B * x) - C\n")
                file.write("Output: Price")
                file.write("Input: x -> miles, thousands\n")
                file.write(f"A: {self.p_opt[0]}\n")
                file.write(f"B: {self.p_opt[1]}\n")
                file.write(f"C: {self.p_opt[2]}\n")
            else:
                pass
