# Example analysis and how to run

Every analysis (small or large) has to be divided into three steps: (the first two of which need to be done only once)

### Create an analysis folder (could copy from testAnalysis to start a basic analysis)
For now we will use the testAnalysis out of the box.

### Creating a one or more sample/process jsons
a sample nanoaod root file to test is here `modules/testsample/tree_6.root`

`python modules/createJSON.py --sampleName test --xsec 1.0 --year 2016 --treename Events --histAxisName test --outname Analysis/testAnalysis/jsons/test.json modules/testsample/`

Add this json in a `sample.txt` file in the analysis folder, which will be input for next step. Example txt file canbe found here: `Analysis/testAnalysis/samples.txt`
If you call it something else other than samples.txt, you can pass it with the --Samples option in the next command.

### Add your analysis to preselector, preprocessor, and analyzer.

### Analyze
 - `preselect`
 - `preprocess`
 - `analyze`

see the script examples from Analysis/testAnalysis (check preselection.py, preprocessor.py, analysis.py)

#### Then run the analysis
`./expresso.py --Analysis testAnalysis --NumberOfTasks 2`

### Make Quick plots

To make quick plots you add a `--QuickPlots` option to the previous command in fact:
`./expresso.py --Analysis testAnalysis --NumberOfTasks 2 --QuickPlots Nele,sumw`

To make more comprehensive plots (multiple backgrounds, signal, data), write a plot file, example `Analysis/ZG/allplots.yaml` allplots.yaml
Then

```
python plot+.py --PlotterScript Analysis/ZG/allplots.yaml --HistoFolder Output/Analysis/ZG/output/analysis/ --SaveLocation Output/Analysis/ZG/output/
```

In the above `--HistoFolder` is where you can find all the histograms, the Analyze step will print this on screen
Check --`SaveLocation` to find your plots