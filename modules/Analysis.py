from coffea import processor,hist
import modules.ExpressoTools as ET
import modules.IHEPProcessor as IHEPProcessor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import json
import logging
import threading
from datetime import datetime
from distutils.dir_util import copy_tree
class IHEPAnalysis:
    
    def __init__(self,name,loglevel=logging.INFO):
        self.a=0
        self.hists={}
        self.samples=[]
        self.SampleList=[]
        self.AnalysisName=name
        self.loglevel=loglevel
        import inspect, logging
    
    def preprocess(self,preprocessor):
        self.preprocess=preprocessor

    def preselection(self,preselection):
        self.preselect=preselection
    
    def SetHists(self,histfile):
        with open(histfile, 'r') as json_file:
            self.hists = json.load(json_file)
            print(self.hists)

    def SetVarsToSave(self,analysis,saveroot):
        def savefunc(logger,events,filename='sample',outputfolder=analysis+'/output/trees/'):
            return "no output file saved"
        self.varstosave=savefunc
        if saveroot:
            savef='Analysis/'+analysis+'/varstosave.py'
            savef=savef.replace(".py","")
            savef=savef.replace("/",".")
            exec(f'from {savef} import varstosave')
            exec('self.varstosave=varstosave')
        
    def GetSamples(self):
        for sami in self.SampleList:
            self.samples.append(ET.parse_yml(sami))
            
    def SetAnalysis(self,analysis,outfolder):
        self.analysis=analysis
        self.outfolder=outfolder
        #return self.logger
    
    def run(self,OutputName,xrootd="root://cmsxrootd.fnal.gov//",chunksize=100,maxchunks=1,saveroot=False):
        
        for sample in self.samples:
            sample["files"]=[xrootd + file for file in sample["files"]]
            dt=datetime.now().strftime("ExpressoJob.d-%d.%m.%Y-t-%H.%M.%S")
            
            
            outfolder=self.outfolder+'/Analysis/'+self.AnalysisName
            logfolder=outfolder+'/logs/'+OutputName+'/'+dt+'/'
            #copy_tree('Analysis/'+self.AnalysisName, logfolder)
            result= processor.run_uproot_job({sample["histAxisName"]:sample["files"]},sample["treeName"],
                                             IHEPProcessor.IHEPProcessor(logfolder,dt,self.loglevel,self.AnalysisName,self.varstosave,
                                                                         self.preprocess,self.preselect,self.analysis,self.hists,sample),
                                             processor.futures_executor,{"schema": NanoAODSchema, 'workers':16} ,
                                             chunksize=chunksize, maxchunks=maxchunks)
            JobFolder=outfolder+'/output/'+OutputName+'/'
            print(f'Your histograms are here:{JobFolder}')
        return result,JobFolder
                       
                         
                          
                         
