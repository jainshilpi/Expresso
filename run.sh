# python Expresso.py --Sample SAMPLES/test.json --OutputFolder /scratch/test/ --ChunkSize 1000 --NumberOfTasks 4 --Analysis chflip -pre Analysis/chflip/preprocessor.py -anascr Analysis/chflip/analysis.py --Xrootd '' --SaveRoot

# python Expresso.py --PlotterScript Analysis/chflip/plot.py --OutputFolder /scratch/test/Analysis/chflip/output/

python Expresso.py --Sample SAMPLES/background_samples/DYJetsToLL_M50.json --OutputFolder /afs/cern.ch/user/a/akapoor/workspace/HEP2022/Expresso/Output/ --ChunkSize 2000 --NumberOfTasks 1 --Analysis chflip -pre Analysis/chflip/preprocessor.py -anascr Analysis/chflip/analysis.py --SaveRoot
