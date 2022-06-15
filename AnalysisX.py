from coffea import processor,hist
import modules.ExpressoTools as ET
import IHEPProcessor as IHEPProcessor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import json
import logging
import threading
from datetime import datetime
from distutils.dir_util import copy_tree

import shutil
import getpass
import os.path

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
    
    def run(self,OutputName,xrootd="root://cmsxrootd.fnal.gov//",chunksize=100,maxchunks=1,saveroot=False):

        for sample in self.samples:
            sample["files"]=[xrootd + file for file in sample["files"]]
            dt=datetime.now().strftime("ExpressoJob.d-%d.%m.%Y-t-%H.%M.%S")
            
            
            outfolder=self.outfolder+'/Analysis/'+self.AnalysisName
            logfolder=outfolder+'/logs/'+OutputName+'/'+dt+'/'
            #copy_tree('Analysis/'+self.AnalysisName, logfolder)
            
            print('{}-wq-coffea'.format(os.environ['USER']))
            executor_args = {
                'master_name': '{}-wq-coffea'.format(os.environ['USER']),
                
                # find a port to run work queue in this range:
                'port': [9123,9130],
                
                'debug_log': 'debug.log',
                'transactions_log': 'tr.log',
                'stats_log': 'stats.log',
                #'environment_file': 'my-coffea-env.tar.gz',
                'extra_input_files': ["IHEPProcessor.py"],#,"modules/ExpressoTools.py","modules/ExpressoPlotTools.py","modules/paths.py"],
                
                'retries': 3,
                
                # use mid-range compression for chunks results. 9 is the default for work
                # queue in coffea. Valid values are 0 (minimum compression, less memory
                # usage) to 16 (maximum compression, more memory usage).
                'compression': 9,
                
                # automatically find an adequate resource allocation for tasks.
                # tasks are first tried using the maximum resources seen of previously ran
                # tasks. on resource exhaustion, they are retried with the maximum resource
                # values, if specified below. if a maximum is not specified, the task waits
                # forever until a larger worker connects.
                'resource_monitor': True,
                'resources_mode': 'auto',
                
                # this resource values may be omitted when using
                # resources_mode: 'auto', but they do make the initial portion
                # of a workflow run a little bit faster.
                # Rather than using whole workers in the exploratory mode of
                # resources_mode: auto, tasks are forever limited to a maximum
                # of 8GB of mem and disk.
                #
                # NOTE: The very first tasks in the exploratory
                # mode will use the values specified here, so workers need to be at least
                # this large. If left unspecified, tasks will use whole workers in the
                # exploratory mode.
                #'cores': 1,
                #'disk': 8000,   #MB
                # 'memory': 10000, #MB
                
                # control the size of accumulation tasks. Results are
                # accumulated in groups of size chunks_per_accum, keeping at
                # most chunks_per_accum at the same time in memory per task.
                'chunks_per_accum': 25,
                'chunks_accum_in_mem': 2,
                
                # terminate workers on which tasks have been running longer than average.
                # This is useful for temporary conditions on worker nodes where a task will
                # be finish faster is ran in another worker.
                # the time limit is computed by multipliying the average runtime of tasks
                # by the value of 'fast_terminate_workers'.  Since some tasks can be
                # legitimately slow, no task can trigger the termination of workers twice.
                #
                # warning: small values (e.g. close to 1) may cause the workflow to misbehave,
                # as most tasks will be terminated.
                #
                # Less than 1 disables it.
                'fast_terminate_workers': 0,
                'wrapper':'wrap',
                'x509_proxy':'/afs/cern.ch/user/a/akapoor/proxy/myx509',
                # print messages when tasks are submitted, finished, etc.,
                # together with their resource allocation and usage. If a task
                # fails, its standard output is also printed, so we can turn
                # off print_stdout for all tasks.
                'verbose': False,
                'print_stdout': False,
            }
            
            executor = processor.work_queue_executor(**executor_args)
            runner = processor.Runner(executor, schema=NanoAODSchema, chunksize=chunksize, maxchunks=maxchunks, skipbadfiles=False, xrootdtimeout=180)
            processor_instance=IHEPProcessor.IHEPProcessor(logfolder,dt,ET,self.loglevel,self.AnalysisName,self.varstosave,
                                                           self.preprocess,self.preselect,self.analysis,self.hists,sample)
            print(f'Before runner')
            result = runner({sample["histAxisName"]:sample["files"]}, sample["treeName"],processor_instance)
            
            JobFolder=outfolder+'/output/'+OutputName+'/'
            print(f'Your histograms are here:{JobFolder}')
        return result,JobFolder
                       
                         
                          
                         
