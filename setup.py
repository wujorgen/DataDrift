from setuptools import find_packages, setup

setup(
    name="DataDrift",
    version="0.0",
    description="",
    author="Jorgen Wu",
    url="",
    packages=find_packages(),
    entry_points={
       'console_scripts': [
           'DataDrift = DataDrift.__init__:main',
       ],
    }
)
