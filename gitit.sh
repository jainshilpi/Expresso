## Test before push
#Env
conda activate py37_coffea_hep
#Analysis
./expresso.py --Sample test_sample.json --Analysis 'testAnalysis' --NumberOfTasks 2
#work_queue_factory -T local -w 10 --cores=10 --memory=8000 --disk=8000 --tasks-per-worker=5 lxplus727.cern.ch 9123
#Plotting
python plot+.py --PlotterScript Analysis/testAnalysis/plot.yaml --HistoFolder ./Output/Analysis/testAnalysis/output/analysis/ --SaveLocation ./Output/Analysis/testAnalysis/output/analysis//plots/
