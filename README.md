# FlatAnalyzer

## Create env

```bash
source BashTools.sh
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
time python Skimmer.py --name DY --file 'root://xrootd-cms.infn.it///eos/cms/store/group/phys_egamma/akapoor/ChargeMisID/newsamples2/06544C90-EFDF-E811-80E6-842B2B6F5D5C.root' --saveroot --outfolder Output --debugprint --analysis TTH --outsuffix DY --multithreaded --xsec 1 --istype mc

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
getremoteskimcommand.sh DY ChargeFlip $PWD/SampleFiles/DYFiles_example.txt TTH
```

## Sanity checks on Skimmed files

There is Info.csv stored in the Skim output folder, that has information on which files at ran on, how many events in total and how many passed, and the name of the corresponding output file. You can run these commands, to extract information from Info.csv

```bash
ReadInfocsv <location of Info.csv>
```

This will give you the command you need to run to submit condor jobs to skim remote files that are stated in $PWD/SampleFiles/DYFiles_example.txt