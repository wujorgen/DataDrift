# DataDrift

DataDrift is a project for scraping vehicle pricing data.
I like data and I like cars, and cars can drift. Sometimes uncontrollably.

## Install Conda
This can be the full version of Anaconda, or Miniconda.

## Create Conda Enviroment
Install the Conda Enviroment in your preferred manner. 

Or, if you are not familiar with Conda, you can run:
- $ conda env create -f ./enviroment.yml -p ./condaenv

The environment can then be activated via:
- $ conda activate ./condaenv

## Installation
To install in editable mode, change to root folder and run:
- $ Pip install -e .
Do not forget the "."

On the todo list is to make a setup file in setup.py or a .toml file so that the DataDrift main driver is accessible from anywhere in the command line.