# setup.py
from setuptools import setup

setup(
    name='modules',
    version='0.0.0',
    description='IHEP Expresso',
    packages=setuptools.find_packages(),
    # Include data files (Note: "include_package_data=True" does not seem to work)
    package_data={
        "modules" : [
            "scripts/*sh",
            "cfg/*.cfg",
            "json/*",
            "data/scaleFactors/*.root",
            "data/fliprates/*.pkl.gz",
            "data/fromTTH/fakerate/*.root",
            "data/fromTTH/lepSF/*/*/*.root",
            "data/fromTTH/lepSF/*/*/*/*.root",
            "data/leptonSF/*/*.root",
            "data/leptonSF/*/*.json",
            "data/triggerSF/*.pkl.gz",
            "data/JEC/*.txt",
            "data/JER/*.txt",
            "data/btagSF/UL/*.pkl.gz",
            "data/btagSF/UL/*.csv",
            "data/btagSF/*.csv",
            "data/pileup/*.root",
            "data/MuonScale/*txt",
            "data/goldenJsons/*.txt",
        ],
    }
)
