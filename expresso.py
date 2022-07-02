#!/usr/bin/env python

####
##  Expresso Framework is designed to perform high energy physics analysis 

if __name__=='__main__':
    
    print('#-----------------------------------------------------------------#')
    import pyfiglet
    print(pyfiglet.figlet_format("Expresso"))
    import os
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    
    
    import argparse
    parser = argparse.ArgumentParser(description='Expresso Framework Options')
    parser.add_argument("--Sample","-s", default='modules/json/background_samples/central_UL/UL18_DY50.json', help = 'path of samples')
    #parser.add_argument("--OutputName","-oN"   , default='results', help = 'Name of output file')
    parser.add_argument("--OutputFolder","-oF"   , default='./', help = 'Path to the output directory')
    parser.add_argument("--ChunkSize","-cs"   , default='./', help = 'chunkSize')
    parser.add_argument("--NumberOfTasks","-Tasks"   , default='./', help = 'threads')
    parser.add_argument("--Analysis","-ana"   , default='chflip', help = 'Analysis name')
    parser.add_argument("--PassOptions","-QSkim"   , default='', help = 'A quick skim')
    parser.add_argument("--ExtraSelection","-QSel"   , default='', help = 'An extra preselection')
    parser.add_argument("--AnalysisScript","-anascr"   , default='Analysis/chflip/analysis.py', help = 'Analysis script')
    parser.add_argument("--Schema","-schema"   , default='NanoAODSchema', help = 'schema')
    parser.add_argument("--PreProcessor","-pre"   , default='pre.py', help = 'preprocessor path')
    parser.add_argument('--SaveRoot', default=False, action='store_true',help = 'save a root tree with branches in varstosave.py')
    parser.add_argument("--Xrootd","-xrd"   , default='root://xrootd-cms.infn.it///', help = 'xrootd redirector')
    parser.add_argument("--Mode","-mode"   , default='local', help = 'mode of running: local, wq')
    parser.add_argument("--Port","-port"   , default='8866', help = 'port of running: wq')
    
    args = parser.parse_args()
    from modules.ExpressoTools import cprint,saveHist
    
    #---------------------------
    cprint(f'Sample will be picked from: {args.Sample}',"OKCYAN")
    cprint(f'Pre-processor will be picked from: {args.PreProcessor}',"OKCYAN")
    cprint(f'Main-analysis will be picked from: {args.AnalysisScript}','OKCYAN')
    cprint(f'#------------------ Performing analysis:','OKBLUE')
    cprint(f'sample->pre-processor->pre-selector->save-root->main-analysis->save-plots','OKBLUE')
    
    #------------------- Initialize an IHEPAnalysis #-------------------###########
    from modules.IHEPAnalysis import IHEPAnalysis
    Ana=IHEPAnalysis(args.Analysis,args.SaveRoot,args.PassOptions)
    
    #---------------------------
    PreProcessor=args.PreProcessor.replace(".py","").replace("/",".")
    exec(f'from {PreProcessor} import preprocess')
    Ana.preprocess(preprocess)
    #---------------------------
    PreSelection='Analysis/'+args.Analysis+'/preselection.py'
    PreSelection=PreSelection.replace(".py","").replace("/",".")
    exec(f"from {PreSelection} import preselection")
    Ana.preselection(preselection,args.ExtraSelection)
    #---------------------------
    #------------------- Initialize the analysis and hists #-------------------###########
    AnalysisPath=args.AnalysisScript.replace(".py","").replace("/",".")
    exec(f"from {AnalysisPath} import histograms,myanalysis")
    Ana.hists=histograms
    Ana.SetAnalysis(myanalysis,args.OutputFolder)
    #---------------------------
    OutputName=(args.AnalysisScript).split('/')[2].replace(".py","")
    print(OutputName)
    #---------------------------
    #------------------- GetTheSamples #-------------------###########
    Ana.SampleList=[args.Sample]
    Ana.GetSamples()
    Ana.SetVarsToSave(args.Analysis)
    #---------------------------
    #------------------- RunYourAnalysis #-------------------###########
    
    result,JobFolder,hname=Ana.run(OutputName=OutputName,xrootd=args.Xrootd,chunksize=int(args.ChunkSize),maxchunks=int(args.NumberOfTasks),
                                   mode=args.Mode, schema=args.Schema, port=int(args.Port))
    #------------------- Save the Histograms #-------------------###########
    if args.PassOptions:
        saveHist(result,JobFolder,hname.replace(" ", "")+'_passoptions='+args.PassOptions)
    else:
        saveHist(result,JobFolder,hname.replace(" ", ""))
    cprint(f'#---- pkl file with results: {JobFolder}/  ----#',"HEADER")
    cprint(f'#---- Make plots: ----#',"OKBLUE")
    cprint(f'#---- python plot+.py --PlotterScript *plot.py --HistoFolder ./* --SaveLocation ./*    ----#',"OKCYAN")
    #------------------- Save the Histograms #-------------------###########
