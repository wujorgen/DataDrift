# DataDrift

DataDrift is a project for scraping vehicle pricing data.
I like data and I like cars, and cars can drift. Sometimes uncontrollably.

## Install Conda
This can be the full version of Anaconda, or Miniconda.

## Create Conda Enviroment
Install the Conda Enviroment in your preferred manner. 

Or, if you are not familiar with Conda, you can run:
```
$ conda env create -f ./enviroment.yml -p ./condaenv
```

The environment can then be activated via:
```
$ conda activate ./condaenv
```

## Installation
To install in editable mode, change to root folder and run:
```
$ pip install -e .
```
Do not forget the "."

To just install the package, only run:
```
$ pip install .
```

## Usage
DataDrift can be called from the command line as follows, given that a "DataDrift.yaml" input file is present in the working directory:
```
$ DataDrift
```

Alternatively, you can use it in your own code:
```
from DataDrift.Drift import Drift
DriftData = Drift()
```
The code above will call the DataDrift library. Then it will look for a input file called "DataDrift.yaml" in the current directory.
Optionally, you can specify the filepath to the input yaml in the constructor argument.
I haven't tested it, but you can also directly feed it a Python dictionary. Will be useful for handling JSON input when this eventually becomes a backend for something...

### Testing
Run either of the following:
```
$ pytest tests
$ pytest --cov=DataDrift tests
```

### Input format
```
"chevrolet": 
  - "camaro"
"ford":
  - "mustang"
  - "f_150"
"toyota": 
  - "camry"
  - "gr_supra"
  - "supra"
"bmw": 
  - "z4"
  - "m240"
  - "m340"
  - "x3"
"audi": 
  - "rs_3"
  - "rs_5"
  - "s5"
"acura":
  - "integra"
  - "tlx"
```