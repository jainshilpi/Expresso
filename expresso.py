#!/usr/bin/env python

####
##  Expresso Framework is designed to perform high energy physics analysis 

if __name__=='__main__':
    import sys
    string_of_command = f"{' '.join(sys.argv)}"
    print('L A U N C H I N G')
    print('#-----------------------------------------------------------------#')
    print(f'python {string_of_command}')
    print('#-----------------------------------------------------------------#')
    import pyfiglet
    from pprint import pprint
    print(pyfiglet.figlet_format("Expresso"))
    import os
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    
    
    import argparse
    parser = argparse.ArgumentParser(description='Expresso Framework Options')
    parser.add_argument("--Samples","-s", default='modules/json/background_samples/central_UL/UL18.txt', help = 'path of samples')
    parser.add_argument("--OutputFolder","-oF"   , default='./Output', help = 'Path to the output directory')
    parser.add_argument("--ChunkSize","-cs"   , default='30000', help = 'chunkSize')
    parser.add_argument("--NumberOfTasks","-Tasks"   , default='./', help = 'threads')
    parser.add_argument("--Analysis","-ana"   , default='chflip', help = 'Analysis name')
    parser.add_argument("--PassOptions","-QSkim"   , default='', help = 'A quick skim')
    parser.add_argument("--ExtraSelection","-QSel"   , default='', help = 'An extra preselection')
    parser.add_argument("--AnalysisScript","-anascr"   , default='', help = 'Analysis script, default Analysis/YourAnalysis/analysis.py')
    parser.add_argument("--Schema","-schema"   , default='NanoAODSchema', help = 'schema')
    parser.add_argument("--PreProcessor","-pre"   , default='', help = 'preprocessor path default Analysis/YourAnalysis/preprocessor.py')
    parser.add_argument("--PreSelector","-preS"   , default='', help = 'preselector path default Analysis/YourAnalysis/preselector.py')
    parser.add_argument('--SaveRoot', default=False, action='store_true',help = 'save a root tree with branches in varstosave.py')
    parser.add_argument("--Xrootd","-xrd"   , default='', help = 'xrootd redirector, example root://xrootd-cms.infn.it///')
    parser.add_argument("--Mode","-mode"   , default='local', help = 'mode of running: local, wq')
    parser.add_argument("--Port","-port"   , default='8866', help = 'port of running: wq')
    parser.add_argument("--Debug",default=False, action='store_true',help = 'if debug')
    
    args = parser.parse_args()
    if args.Debug: pprint(vars(args))
        
    from modules.ExpressoTools import cprint,saveHist
    
    #---------------------------
    if not args.PreSelector:
        PreSelection='Analysis/'+args.Analysis+'/preselection.py'
    else:
        PreSelection=args.PreSelector

    if not args.PreProcessor:
        PreProcessor='Analysis/'+args.Analysis+'/preprocessor.py'
    else:
        PreProcessor=args.PreProcessor
        
    if not args.AnalysisScript:
        AnalysisScript='Analysis/'+args.Analysis+'/analysis.py'
    else:
        AnalysisScript=args.AnalysisScript
        
    cprint(f'Samples will be picked from: {args.Samples}',"OKCYAN")
    cprint(f'Pre-processor will be picked from: {PreProcessor}',"OKCYAN")
    cprint(f'Pre-selector will be picked from: {PreSelection}',"OKCYAN")
    cprint(f'Main-analysis will be picked from: {AnalysisScript}','OKCYAN')
    cprint(f'#------------------ Performing analysis:','OKBLUE')
    cprint(f'sample->pre-processor->pre-selector->save-root->main-analysis->save-plots','OKBLUE')
    
    #------------------- Initialize an IHEPAnalysis #-------------------###########
    from modules.IHEPAnalysis import IHEPAnalysis
    Ana=IHEPAnalysis(args.Analysis,args.SaveRoot,args.PassOptions,args.Debug)
    
    #---------------------------
    PreProcessor=PreProcessor.replace(".py","").replace("/",".")
    exec(f'from {PreProcessor} import preprocess')
    Ana.preprocess(preprocess)
    #---------------------------
    #PreSelection='Analysis/'+args.Analysis+'/preselection.py'
    PreSelection=PreSelection.replace(".py","").replace("/",".")
    exec(f"from {PreSelection} import preselection")
    Ana.preselection(preselection,args.ExtraSelection)
    #---------------------------
    #------------------- Initialize the analysis and hists #-------------------###########
    AnalysisPath=AnalysisScript.replace(".py","").replace("/",".")
    exec(f"from {AnalysisPath} import histograms,myanalysis")
    Ana.hists=histograms
    Ana.SetAnalysis(myanalysis,args.OutputFolder)
    #---------------------------
    OutputName=(AnalysisScript).split('/')[2].replace(".py","")
    #---------------------------
    #------------------- GetTheSamples #-------------------###########
    my_file = open(str(args.Samples), "r")
    sampledata = my_file.read()
    print(f'reading:')
    print(f'{sampledata}')
    SampleList=sampledata.split("\n")
    Ana.SampleList = [i for i in SampleList if i]
    Ana.GetSamples()
    Ana.SetVarsToSave(args.Analysis)
    #---------------------------
    #------------------- RunYourAnalysis #-------------------###########
    if args.Debug: pprint(vars(Ana))
    runresults=Ana.run(OutputName=OutputName,xrootd=args.Xrootd,chunksize=int(args.ChunkSize),maxchunks=int(args.NumberOfTasks),
                                   mode=args.Mode, schema=args.Schema, port=int(args.Port))
    if args.Debug: pprint(vars(Ana))

    for result,JobFolder,hname in runresults: 
        #------------------- Save the Histograms #-------------------###########
        if args.PassOptions:
            saveHist(result,JobFolder,hname.replace(" ", "")+'_passoptions='+args.PassOptions)
        else:
            saveHist(result,JobFolder,hname.replace(" ", ""))
    cprint(f'#---- pkl files with results: {JobFolder}/  ----#',"HEADER")
    cprint(f'#---- Make plots: ----#',"OKBLUE")
    cprint(f'#---- python plot+.py --PlotterScript *plot.py --HistoFolder ./* --SaveLocation ./*    ----#',"OKCYAN")
    #------------------- Save the Histograms #-------------------###########
