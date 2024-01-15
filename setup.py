from setuptools import find_packages, setup

setup(
    name="DataDrift",
    version="1.0",
    description="DataDrift scrapes car pricing information.",
    author="Jorgen Wu",
    url="https://github.com/wujorgen/DataDrift",
    packages=find_packages(),
    entry_points={
       'console_scripts': [
           'DataDrift = DataDrift.__init__:main',
       ],
    }
)
