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
    try:
        import pyfiglet
        print(pyfiglet.figlet_format("Expresso"))
    except:
        print(" E X P R E S S O")
    import os
    from pprint import pprint
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    import yaml
    
    import argparse
    parser = argparse.ArgumentParser(description='Expresso Framework Options')
    parser.add_argument("--Samples","-s", default='', help = 'path of samples')
    parser.add_argument("--QuickPlots","-qp", default='', help = 'some quick plots')
    parser.add_argument("--FullPlots","-fp", default='', help = 'full plots')
    parser.add_argument("--OutputFolder","-oF"   , default='./Output', help = 'Path to the output directory')
    parser.add_argument("--ChunkSize","-cs"   , default='30000', help = 'chunkSize')
    parser.add_argument("--NumberOfTasks","-Tasks"   , default='2', help = 'threads')
    parser.add_argument("--Analysis","-ana"   , default='chflip', help = 'Analysis name')
    parser.add_argument("--PassOptions","-QSkim"   , default='', help = 'A quick skim')
    parser.add_argument("--ExtraSelection","-QSel"   , default='', help = 'An extra preselection')
    parser.add_argument("--AnalysisPoint","-ASel"   , default='', help = 'A analysis point customizable')
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

    
    anasplit=args.Analysis.split('/')
    if anasplit[0]=='Analysis':
        args.Analysis=anasplit[1]
    if not args.Samples:
        args.Samples="Analysis/"+args.Analysis+"/samples.txt"    
    
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
    Ana.preselection(preselection,args.ExtraSelection,args.AnalysisPoint)
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
        histfilename=hname.replace(" ", "")
        
        if args.PassOptions:
            histfilename=histfilename+'_passop_'+args.PassOptions
        if args.AnalysisPoint:
            histfilename=histfilename+'_anap_'+args.AnalysisPoint
            
        histfilename=histfilename+".pkl.gz"
        saveHist(result,JobFolder,histfilename)

        cprint(f'#---- pkl files with results: {JobFolder}/{histfilename}  ----#',"HEADER")
        cprint(f'#---- Make plots: ----#',"OKBLUE")
        cprint(f'#---- python plot+.py --PlotterScript *plot.py --HistoFolder ./* --SaveLocation ./*    ----#',"OKCYAN")
        cprint(f'#---- Analysis done! ----#',"OKBLUE")
        if args.QuickPlots:
            try:
                cprint(f'########## Quick Plotting turned on #############',"HEADER")
                Plots=args.QuickPlots.split(',')
                Plotnames=["normal_"+p for p in Plots]
                plotdict={}
                plotdict['plots']={}
                for i,pl in enumerate(Plots):
                    plotdict['plots'][str(Plotnames[i])]=str(pl)
                    plotdict['2016']={'filename':histfilename+',red,nostack,1'}

                Histolist='Analysis/'+args.Analysis+'/temp.yaml'
                Histofolder=JobFolder
                Savefolder=args.OutputFolder+'/Analysis/'+args.Analysis+'/output/analysis/'+hname+'/'
                with open(Histolist, 'w') as f:
                    yaml.dump(plotdict, f, default_flow_style=False)

                print(f'Histograms picked from {Histofolder}')
                cprint(f'QuickPlot option should only be used for quick single sample plotting!',"OKCYAN")
                cprint(f'For detailed plotting with multiple samples, run the analysis jobs and then use plot+.py by passing yaml like this:',"OKCYAN")
                print(yaml.dump(plotdict, default_flow_style=False))
                cprint(f'########## Making some quick plots #############',"HEADER")
                os.system('python plot+.py --PlotterScript '+Histolist+' --HistoFolder '+Histofolder+'/ --SaveLocation '+Savefolder)
            except Exception as e:
                cprint(f'########## Quick Plotting did not work! #############',"HEADER")
                print(e)

        if args.FullPlots:
            try:
                cprint(f'########## Full Plotting turned on #############',"HEADER")
            
                Histolist=args.FullPlots
                Histofolder=JobFolder
                Savefolder=args.OutputFolder+'/Analysis/'+args.Analysis+'/output/analysis/'

                print(f'Histograms picked from {Histofolder}')
                os.system('python plot+.py --PlotterScript '+Histolist+' --HistoFolder '+Histofolder+'/ --SaveLocation '+Savefolder)
            except Exception as e:
                cprint(f'########## Full Plotting did not work! #############',"HEADER")
                print(e)
