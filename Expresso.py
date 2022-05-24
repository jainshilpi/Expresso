#!/usr/bin/env python

import awkward as ak
import uproot
import coffea as coffea
from coffea import hist
uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource

import modules.Analysis as Analysis
import modules.ExpressoTools as ET
from modules.selection import *
from coffea.analysis_tools import PackedSelection

import argparse
parser = argparse.ArgumentParser(description='Expresso Framework Options')
parser.add_argument("--Sample","-s", default='modules/json/background_samples/central_UL/UL18_DY50.json', help = 'path of samples')
parser.add_argument("--OutputName","-oN"   , default='results', help = 'Name of output file')
parser.add_argument("--OutputFolder","-oF"   , default='./', help = 'Path to the output directory')
parser.add_argument("--ChunkSize","-cs"   , default='./', help = 'chunkSize')
parser.add_argument("--NumberOfTasks","-Tasks"   , default='./', help = 'threads')
parser.add_argument("--Analysis","-ana"   , default='chflip', help = 'Analysis name')
parser.add_argument("--PreProcessor","-pre"   , default='pre.py', help = 'preprocessor path')
#parser.add_argument("--PreSelection","-pre"   , default='sel.py', help = 'preselection')
parser.add_argument("--PlotterScript","-plotter"   , default='', help = 'plotterscript')

args = parser.parse_args()


ET.cprint(f'#----------------- E X P R E S S O    F R A M E W O R K-------------------#',"HEADER")
ET.cprint(f'Sample will be picked from: {args.Sample}',"OKCYAN")
ET.cprint(f'Pre-processor will be picked from: {args.PreProcessor}',"OKCYAN")
ET.cprint(f'Main-analysis will be picked from: Analysis/{args.Analysis}/analysis.py','OKCYAN')

ET.cprint(f'#------------------ Performing analysis:','OKBLUE')
ET.cprint(f'sample->pre-processor->pre-selector->main-analysis->save-plots->draw-plots','OKBLUE')
ET.cprint(f'#----------------- E X P R E S S O    F R A M E W O R K-------------------#',"HEADER")

PreProcessor=args.PreProcessor
PreProcessor=PreProcessor.replace(".py","")
PreProcessor=PreProcessor.replace("/",".")
exec(f"from {PreProcessor} import preprocess")


PreSelection='Analysis/'+args.Analysis+'/preselection.py'
PreSelection=PreSelection.replace(".py","")
PreSelection=PreSelection.replace("/",".")
exec(f"from {PreSelection} import preselection")

AnalysisPath='Analysis/'+args.Analysis+'/analysis.py'
AnalysisPath=AnalysisPath.replace(".py","")
AnalysisPath=AnalysisPath.replace("/",".")
exec(f"from {AnalysisPath} import histograms,myanalysis")

#------------------- Initialize an IHEPAnalysis #-------------------###########
Ana=Analysis.IHEPAnalysis()
#------------------- Initialize the hists #-------------------###########
Ana.hists=histograms
#------------------- GetTheSamples #-------------------###########
Ana.SampleList=[args.Sample]
Ana.GetSamples()

Ana.preprocess(preprocess)
Ana.preselection(preselection)
#------------------- SetYourAnalysis #-------------------###########
Ana.SetAnalysis(myanalysis)
#------------------- RunYourAnalysis #-------------------###########
result=Ana.run(chunksize=int(args.ChunkSize),maxchunks=int(args.NumberOfTasks))
#------------------- Save the Histograms #-------------------###########
ET.saveHist(result,args.OutputFolder,args.OutputName)
ET.cprint(f'#---- pkl file with results: {args.OutputFolder}/  ----#',"HEADER")
#------------------- Save the Histograms #-------------------###########
if args.PlotterScript:
    print("Plotter Option is under dev")
