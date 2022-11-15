import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from coffea import processor#,hist
import modules.ExpressoTools as ET
import modules.IHEPProcessor as IHEPProcessor
from coffea.nanoevents import NanoAODSchema
import json
import logging
import threading
from datetime import datetime
from distutils.dir_util import copy_tree
import shutil
import getpass
import os.path
from modules.wq import WQ
from objprint import add_objprint,op
from objprint import config
config(depth=1000)
config(indent=4)

class IHEPAnalysis:

    def __init__(self,name,saveroot,passoptions,debug=False,loglevel=logging.INFO):


        self.a=0
        self.hists={}
        self.samples=[]
        self.SampleList=[]
        self.AnalysisName=name
        self.saveroot=saveroot
        self.passoptions=passoptions
        self.debug=debug
        self.loglevel=loglevel
        import inspect, logging

    def preprocess(self,preprocessor):
        self.preprocess=preprocessor

    def preselection(self,preselection,extraselection):
        self.preselect=preselection
        self.extraselection=extraselection
        

    def SetHists(self,histfile):
        with open(histfile, 'r') as json_file:
            self.hists = json.load(json_file)
            print(self.hists)

    def SetVarsToSave(self,analysis):
        saveroot=self.saveroot
        def savefunc(threadn,logger,events,filename='sample',outputfolder=analysis+'/output/trees/'):
            return filename,events[0>1]
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

    def run(self,OutputName,xrootd="root://cmsxrootd.fnal.gov//",chunksize=100,maxchunks=1,mode='local',schema='NanoAODSchema',port=8865):
        import time
        tstart = time.time()

        #for sample in self.samples:
        sample=self.samples[0]
        sample["files"]=[xrootd + file for file in sample["files"]]
        dt=datetime.now().strftime("ExpressoJob.d-%d.%m.%Y-t-%H.%M.%S")
        outfolder=self.outfolder+'/Analysis/'+self.AnalysisName
        logfolder=outfolder+'/logs/'+OutputName+'/'+dt+'/'
        treefolder=outfolder

        import uproot
        uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource

        if mode=='wq' or mode=='condor' or mode=='sq':
            mastername='{}-wq-coffea'.format(os.environ['USER'])
            print(mastername)
            ar={'master_name':mastername,
                'port':port,
                'wrapper':'/afs/ihep.ac.cn/users/k/kapoor/wrap.sh'
            }
            MyWQ=WQ(ar).getwq()
            print(MyWQ)
            executor = processor.work_queue_executor(**MyWQ)
            #import subprocess
            #print("Submitting condor jobs")
            #scratchdi="./workers/wq_"+dt
            #subprocess.call("mkdir -p "+scratchdi, shell=True)
            #gpujob="work_queue_factory -M "+mastername+" --scratch-dir "+scratchdi+"  -T slurm -B --partition=gpu &> "+scratchdi+"/gpu.log &"
            #spubjob="work_queue_factory -M "+mastername+" --scratch-dir "+scratchdi+"  -T slurm -B --partition=spub &> "+scratchdi+"/spub.log &"
            #subprocess.call(gpujob, shell=True)
            #subprocess.call(spubjob, shell=True)
            print("Submitted worker jobs------ Now Collecting")


        if mode=='dask':
            from dask.distributed import Client
            client = Client(os.environ['DASK_SCHEDULER'])
            config = {
                'client': client,
                'compression': 1,
            }
            executor = processor.DaskExecutor(**config)

        if mode=='local':

            ar={'workers':20}
            executor = processor.futures_executor(**ar)


        Schema=NanoAODSchema
        exec('Schema='+schema)
        runner = processor.Runner(executor, schema=Schema, chunksize=chunksize, maxchunks=maxchunks, skipbadfiles=False, xrootdtimeout=360)
        processor_instance=IHEPProcessor.IHEPProcessor(logfolder,treefolder,dt,ET,self.loglevel,self.AnalysisName,self.varstosave,
                                                       self.preprocess,self.preselect,self.analysis,self.hists,sample,self.saveroot,self.passoptions,self.extraselection,self.debug)
        if self.debug:
            op(processor_instance)

        result = runner({sample["histAxisName"]:sample["files"]}, sample["treeName"],processor_instance)
        JobFolder=outfolder+'/output/'+OutputName+'/'
        print(f'Your histograms are here:{JobFolder}')
        elapsed = time.time() - tstart
        minutes = elapsed // 60 % 60
        seconds = elapsed % 60
        print(f'Elapssed Time: {minutes} minutes {seconds} seconds')
        return result,JobFolder,sample["histAxisName"]

if __name__=='__main__':
    print("Hello, this script is not meant to be run by itself.")
