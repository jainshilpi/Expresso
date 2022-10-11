#work_queue_factory -T local -w 10 --cores=10 --memory=8000 --disk=8000 --tasks-per-worker=5 lxplus727.cern.ch 9123
conda activate py37_coffea_hep
./expresso.py \
    --Sample test_sample.json\
    --ChunkSize 10000 \
    --NumberOfTasks $1 \
    --Analysis chflip \
    -pre Analysis/chflip/preprocessor.py \
    -anascr Analysis/chflip/analysis.py \
    --Xrootd '' \
    --OutputFolder ./Output

python plot+.py --PlotterScript Analysis/chflip/plot.yaml --HistoFolder ./Output/Analysis/chflip/output/analysis/ --SaveLocation ./Output/Analysis/chflip/output/analysis//plots/
