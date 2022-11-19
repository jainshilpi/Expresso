## The basic setup is:

for this setup I have stored my Nanoaod files here `/scratch/zg/GluGluHToZG_ZToLL_M-120_TuneCP5_13TeV-powheg-pythia/` in my computer. Depending upon your path things might change

a) create one or more sample jsons (mostly needed to be done only when you indtroduce a new sample or change sample location etc.)
eg.
```
python modules/createJSON.py --sampleName ZG --xsec 1.0 --year 2016 --treename Events --histAxisName ZG --outname Analysis/ZG/jsons/ZG.json /scratch/zg/GluGluHToZG_ZToLL_M-120_TuneCP5_13TeV-powheg-pythia/
```

Check Analysis/ZG/jsons/ZG.json, now add all the jsons you want to run on in a txt file
Check Analysis/ZG/jsons/ZG.txtx

### Analyze
 - preselect
 - preprocess
 - analyze

see the script examples from Analysis/ZG (check preselection.py, preprocessor.py, analysis.py)

Then just say

```
./expresso.py --Samples ZG.txt --Analysis ZG --NumberOfTasks 2
```

### Make plots
Write a plot file, example Analysis/ZG/allplots.yaml allplots.yaml
Then

```
python modules/dump_plotyaml.py Analysis/ZG/allplots.yaml > Analysis/ZG/plots.yaml
python plot+.py --PlotterScript Analysis/ZG/plots.yaml --HistoFolder Output/Analysis/ZG/output/analysis/ --SaveLocation Output/Analysis/ZG/output/
```

In the above --HistoFolder is where you can find all the histograms, the Analyze step with print this on screen
Check --SaveLocation to find your plots