# Setup

`. setup.sh`

# Example analysis and how to run

Every analysis (small or large) has to be divided into three steps: (the first two of which need to be done only once)

### Create an analysis folder in Analysis/ (could copy from barebones to start a basic analysis)
For now we will use the barebones out of the box.

### Creating a one or more sample/process jsons
a sample nanoaod root file to test is here `modules/testsample/tree_6.root`

`python modules/createJSON.py --sampleName test --xsec 1.0 --year 2016 --treename Events --histAxisName test --outname Analysis/barebones/jsons/test.json modules/testsample/`

Add this json in a `sample.txt` file in the analysis folder, which will be input for next step. Example txt file canbe found here: `Analysis/barebones/samples.txt`
If you call it something else other than samples.txt, you can pass it with the `--Samples` option in the next command.

If you just want to pass a single json, you can pass it using `--Sample bla-bla/bla-bla/something.json`

#### Creating JSON's to run on samples remotely:
##### Putting an example here for dataset
`/GluGluHToZGToMuMuG_M125_MLL-50To1000_012j_13TeV_amcatnloFXFX_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM`
```
python modules/createJSON.py --prefix root://cms-xrd-global.cern.ch// --sampleName GluGluHToZG --year 2016 --treename Events --histAxisName GluGluHToZG --xsec 2 --DAS --outname test.json /GluGluHToZGToMuMuG_M125_MLL-50To1000_012j_13TeV_amcatnloFXFX_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM
```

### Add your analysis to preselector, preprocessor, and analyzer.

### Analyze
 - `preselect`
 - `preprocess`
 - `analyze`

see the script examples from Analysis/barebones (check preselection.py, preprocessor.py, analysis.py)

#### Then run the analysis, can run in several ways:
```
./expresso.py --Analysis barebones --NumberOfTasks 2 --AnalysisPoint tight_ele_tight_mu
```

```
./expresso.py --Analysis barebones --NumberOfTasks 2
```

The `--AnalysisPoint` argument is a string is available to be used to your scripts to that you can customize what you want to do
See example in Analysis/barebones (check preselection.py, preprocessor.py, analysis.py). This is an optional argument.

To debug
```
./expresso.py --Analysis barebones --NumberOfTasks 2 --Debug
```

To pass some options can be used as strings to use in scripts, similar to analysis point.

```
./expresso.py --Analysis barebones --NumberOfTasks 2 --PassOptions 2e2u` ## This will do nothing as nothing is defined, but in analysis.py, you can write what to do if PassOptions is `2e2u
```


### Make Quick plots along with the analysis

To make quick plots you add a `--QuickPlots` option to the previous command in fact:

```.
/expresso.py --Analysis barebones --NumberOfTasks 2 --AnalysisPoint tight --QuickPlots Nele,sumw
```

To make more comprehensive plots (multiple backgrounds, signal, data), write a plot file, example `Analysis/ZG/allplots.yaml` allplots.yaml
Then run

```
python plot+.py --PlotterScript Analysis/barebones/allplots.yaml --HistoFolder Output/Analysis/barebones/output/analysis/ --SaveLocation Output/Analysis/barebones/output/analysis/
```

In the above `--HistoFolder` is where you can find all the histograms that are loaded in `--PlotterScript`, the Analyze step will print this histogram location on screen.
Check --`SaveLocation` to find your plots

### How to customize `--PlotterScript`

The plotter script has two parts, year and plots.
A simple script is:
`
'2016':
  HG: test_anap_tight.pkl.gz,red,nostack,1
plots:
  normal_Nele: Nele
`
This means the plots will have a label 2016, and use one file `test_anap_tight.pkl.gz`, with label `HG` on plots and will plot histogram `Nele` from the file. Color will be read, plot won't be stacked and will be scaled by `1`. `normal` is a keyword. Please use this as is.

Other possible example:
```
'2018':
  DY: DY_anap_loose.pkl.gz,green,stack,1
  ZG: ZG_anap_loose.pkl.gz,blue,stack,1
  data: data_anap_loose.pkl.gz,black,nostack,1
plots:
  normal_Nele: Nele
```

To normalize a plot to just see the shape, you can use a scale of `-1`


