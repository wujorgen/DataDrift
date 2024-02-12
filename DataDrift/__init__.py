"""
DataDrift

DataDrift is a data mining and analysis tool for vehicle pricing.

Classes:
- Drift: The main driver of the program. Contains scraping and input reading logic.
- DriftCar: The object representing a car. Contains data cleaning and writing logic.

"""

from .Drift import Drift
from .DriftCar import DriftCar  # noqa F401


def main():
    DriftData = Drift()  # noqa F841
    breakpoint()
