# FlatAnalyzer

## Create env
source /cvmfs/sft.cern.ch/lcg/views/LCG_98py3cu10/x86_64-centos7-gcc8-opt/setup.sh

## Create Analyzer

jupyter nbconvert --to script Analyzer.ipynb

## Basic usage

python Analyzer.py --name 'DY' --file 'root://xrootd-cms.infn.it///store/mc/RunIIFall17NanoAODv7/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017RECOSIMstep_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/110000/12AAE61E-F886-B24E-8F62-57765FBC2CE9.root' --saveroot --outfolder 'ChargeFlip' --outsuffix 'skim' --branchlist '(ChargeFlip_Category|MyElectron_eta|MyElectron_pt)'