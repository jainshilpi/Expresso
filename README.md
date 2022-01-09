# FlatAnalyzer

## Create env
source /cvmfs/sft.cern.ch/lcg/views/LCG_98py3cu10/x86_64-centos7-gcc8-opt/setup.sh

##Create Analyzer

jupyter nbconvert --to script Analyzer.ipynb

## Basic usage

python Analyzer.py --name DY --file DYfiles/sample*root