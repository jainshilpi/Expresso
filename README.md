# FlatAnalyzer

## Create env

```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_98py3cu10/x86_64-centos7-gcc8-opt/setup.sh
```

## Create Analyzer

```bash
jupyter nbconvert --to script Skimmer.ipynb
jupyter nbconvert --to script Analyzer.ipynb

```

## Check basic options

```bash
python Skimmer.py -h
python Analyzer.py -h
````


## Basic interactive usage (also possible to run on remote files interactively, if proxy is generated)

### Skimming
```bash
python Skimmer-new.py --name DY --file 'root://xrootd-cms.infn.it///store/mc/RunIIFall17NanoAODv7/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANO\
AODSIM/PU2017RECOSIMstep_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/110000/12AAE61E-F886-B24E-8F62-57765FBC2CE9.root' --saveroot --outfolder Output --debugprint --analysis TTH --saveroot --outsuffix DY"

```

### Analysis
```bash
time python Analyzer.py --name 'DY' --file ChargeFlip/output_skim.root --outfolder ChargeFlip_plots

```

## Submitting remote jobs (example)

The first thing you need to do is to change the location of you proxy (needs to be somewhere in $home), so you should add such a line in your .bashrc file (this is an example for my area, you can give your location somewhere in your home area)

```
export X509_USER_PROXY=/afs/cern.ch/user/a/akapoor/proxy/myx509

```

Run this command in your terminal
```bash
. getremoteskimcommand.sh DY ChargeFlip $PWD/SampleFiles/DYFiles_example.txt
```

This will give you the command you need to run to submit condor jobs to skim remote files that are stated in $PWD/SampleFiles/DYFiles_example.txt