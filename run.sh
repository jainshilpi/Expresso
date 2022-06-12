python Expresso.py --Sample SAMPLES/test.json --OutputFolder /scratch/test/ --ChunkSize 1000 --NumberOfTasks 4 --Analysis chflip -pre Analysis/chflip/preprocessor.py -anascr Analysis/chflip/analysis.py --Xrootd '' --SaveRoot

python Expresso.py --PlotterScript Analysis/chflip/plot.py --OutputFolder /scratch/test/Analysis/chflip/output/
