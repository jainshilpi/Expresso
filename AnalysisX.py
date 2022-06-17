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
        def savefunc(threadn,logger,events,filename='sample',outputfolder=analysis+'/output/trees/'):
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
    
    def run(self,OutputName,xrootd="root://cmsxrootd.fnal.gov//",chunksize=100,maxchunks=1,saveroot=False,mode='local',schema='NanoAODSchema'):
        import time
        tstart = time.time()
        
        for sample in self.samples:
            sample["files"]=[xrootd + file for file in sample["files"]]
            dt=datetime.now().strftime("ExpressoJob.d-%d.%m.%Y-t-%H.%M.%S")
            
            
            outfolder=self.outfolder+'/Analysis/'+self.AnalysisName
            logfolder=outfolder+'/logs/'+OutputName+'/'+dt+'/'
            #copy_tree('Analysis/'+self.AnalysisName, logfolder)
            
            import uproot
            uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource
            
            if mode=='wq':
                mastername='{}-wq-coffea'.format(os.environ['USER'])
                print(mastername)
                ar={'master_name':mastername,
                    'port':8787,
                    #'password_file':os.getcwd()+'pass.txt',
                      #'wrapper':'wrap',
                      #'x509_proxy':'/afs/cern.ch/user/a/akapoor/proxy/myx509'}
                    }
                MyWQ=WQ(ar).getwq()
                print(MyWQ)
                executor = processor.work_queue_executor(**MyWQ)

            if mode=='dask':
                from dask.distributed import Client
                #from dask_jobqueue.htcondor import HTCondorCluster
                
                #cluster = HTCondorCluster(
                #    job_extra={
                #        'GetEnv':'false',
                #        'universe':'vanilla',
                #        'Output':'logs/$(Name).out',
                #        'Error': 'logs/$(Name).err',
                #        'Log' : 'logs/$(Name).log',
                #        'should_transfer_files' : 'YES',
                #        'when_to_transfer_output' :'ON_EXIT'
                #    },
                #    local_directory=os.getcwd()+'/workers',
                #    env_extra=[
                #        'source /afs/cern.ch/user/a/akapoor/.bashrc',
                #        'cd /afs/cern.ch/user/a/akapoor/workspace/HEP2022/Expresso',
                #        'source /cvmfs/sft.cern.ch/lcg/views/dev3cuda/latest/x86_64-centos7-gcc8-opt/setup.sh',
                #        'pip install -e .'
                #    ],
                #    log_directory=os.getcwd()+'/workers',
                #    cores=24,
                #    memory="4GB", 
                #    disk="4GB")
                
                #cluster.scale(jobs=10)
                
                client = Client(os.environ['DASK_SCHEDULER'])
                # mastername='{}-wq-coffea'.format(os.environ['USER'])
                # print(mastername)
                config = {
                    'client': client,
                    'compression': 1,
                    #'savemetrics': 1,
                    # 'xrootdconfig': {
                    #     'chunkbytes': 1024*128,
                    #     'limitbytes': 200 * 1024**2
                    # },
                    #'cachestrategy': 'dask-worker',
                    #'worker_affinity': True,
                }
                executor = processor.DaskExecutor(**config)
                
            if mode=='local':
                
                ar={'workers':20}
                executor = processor.futures_executor(**ar)
            Schema=NanoAODSchema
            exec('Schema='+schema)
            runner = processor.Runner(executor, schema=Schema, chunksize=chunksize, maxchunks=maxchunks, skipbadfiles=False, xrootdtimeout=500)
            processor_instance=IHEPProcessor.IHEPProcessor(logfolder,dt,ET,self.loglevel,self.AnalysisName,self.varstosave,
                                                           self.preprocess,self.preselect,self.analysis,self.hists,sample)
            result = runner({sample["histAxisName"]:sample["files"]}, sample["treeName"],processor_instance)
            JobFolder=outfolder+'/output/'+OutputName+'/'
            print(f'Your histograms are here:{JobFolder}')
        elapsed = time.time() - tstart
        print(f'Elapssed Time:{elapsed}')
        return result,JobFolder
                       
                         
                          
                         
