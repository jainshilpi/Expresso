# Welcome to Expresso documentation

Expresso is based on [coffea](https://coffeateam.github.io/coffea/), wrapped with functionalities to share analysis methods between different analysis teams, proper logging support and ability to save the status of the analysis at various stages like preselection, preprocessing etc.

#### Step 1: User issues one or more commands for different processes
example:
```
./expresso.py --Sample DYsample.json --Analysis 'testAnalysis' --NumberOfTasks 2
./expresso.py --Sample TTsample.json --Analysis 'testAnalysis' --NumberOfTasks 2
```

``` mermaid
graph LR
  A(Sample files) --> C(expresso.py)
  B(Analysis files) --> C(expresso.py)
  C --> |Multiprocessing| D(pre processor)
  D --> E(pre selector)
  E --> F(save root file)
  E --> G(main analysis)
  G --> H(output)
```

#### Step 2: User makes plots
example:
```
./plot+.py --PlotterScript Analysis/testAnalysis/plot.yaml --HistoFolder ./Output/Analysis/testAnalysis/output/analysis/
```
``` mermaid
graph LR
  H(output) --> I(plot+.py)
  I --> J(make plots)
  
```