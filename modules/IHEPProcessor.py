from coffea import processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import hist
import threading
import logging
import modules.ExpressoTools as ET
import traceback
import ctypes
libc = ctypes.cdll.LoadLibrary('libc.so.6')
SYS_gettid = 186
import os
from datetime import datetime
import pwd
import platform
import sys
import glob
import awkward as ak
import numpy as np

class IHEPProcessor(processor.ProcessorABC):
    def __init__(self,outfolder,dt,loglevel,analysisname,varstosave,preprocess,preselect,analysis,histos,samples):
        histos['sumw']=hist.Hist(axes=[hist.Bin("sumw", "sumw", 10, 0, 10)],
                                 label="sumw")
        histos['cutflow']=hist.Hist(axes=[hist.Cat("selection", "selection"),
                                          hist.Bin("x", "x coordinate [m]", 80, 0, 80)],
                                    label="Cutflow")
        histos['events_processed']=hist.Hist(axes=[hist.Bin("events_processed", "events_processed", 2, 0, 2)],label="events_processed")
        self._accumulator = processor.dict_accumulator(histos)
        self._samples = samples
        self._analysis = analysis
        self._preprocess = preprocess
        self._preselect = preselect
        self._varstosave = varstosave
        self._analysisname = analysisname
        self._loglevel=loglevel
        self._dt = dt
        self._outfolder=outfolder
        self._summarylog=outfolder+"/log/summary.log"
        if not os.path.isdir(outfolder+"/log"): os.makedirs(outfolder+"/log")
        try:
            open(self._summarylog, 'a').close()
        except OSError:
            print('creating summary log')
        else:
            print('summary log created')

        def summary(summarylog,message,lastline=False):
            message=message+" "
            with open(summarylog, 'a') as f:
                if not lastline:
                    print(message, file=f, end =" ")
                else:
                    print(message, file=f)
        #self._summary(self._summarylog,f'sub-job_{threadn}',firstline=True)
        self._summary=summary
        
    @property
    def accumulator(self):
        return self._accumulator

    # def summary(self,message,firstline=False):
    #     message=message+" "
    #     with open(self._summarylog, 'w') as f:
    #         if not firstline:
    #             print(message, file=f, end =" ")
    #         else:
    #             print(message, file=f)

    # we will receive a NanoEvents instead of a coffea DataFrame
    def process(self, events):
        logger = logging.getLogger(__name__)
        logger.setLevel(self._loglevel)
        threadn=libc.syscall(SYS_gettid)
        # Create handlers
        logpath=self._outfolder+'/log/sub-job_'+str(threadn)
        if not os.path.isdir(logpath): os.makedirs(logpath)
        debug_handler = logging.FileHandler(logpath+'/logfile_debug.log')
        info_handler = logging.FileHandler(logpath+'/logfile_info.log')
        warning_handler = logging.FileHandler(logpath+'/logfile_warning.log')
        error_handler = logging.FileHandler(logpath+'/logfile_error.log')
        sys.stdout = open(logpath+'/logfile_stdout.log', 'w')
        sys.stderr = open(logpath+'/logfile_stderr.log', 'w')
        debug_handler.setLevel(logging.DEBUG)
        info_handler.setLevel(logging.INFO)
        warning_handler.setLevel(logging.WARNING)
        error_handler.setLevel(logging.ERROR)
        # Create formatters and add it to handlers
        info_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        warning_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        debug_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        error_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        info_handler.setFormatter(info_format)
        debug_handler.setFormatter(debug_format)
        warning_handler.setFormatter(warning_format)
        error_handler.setFormatter(error_format)

        # Add handlers to the logger
        logger.addHandler(debug_handler)
        logger.addHandler(info_handler)
        logger.addHandler(warning_handler)
        logger.addHandler(error_handler)
        self._logger=logger
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        ET.autolog('███████ ██   ██ ██████  ██████  ███████ ███████ ███████  ██████  ',self._logger,'i')
        ET.autolog('██       ██ ██  ██   ██ ██   ██ ██      ██      ██      ██    ██ ',self._logger,'i')
        ET.autolog('█████     ███   ██████  ██████  █████   ███████ ███████ ██    ██ ',self._logger,'i')
        ET.autolog('██       ██ ██  ██      ██   ██ ██           ██      ██ ██    ██ ',self._logger,'i')
        ET.autolog('███████ ██   ██ ██      ██   ██ ███████ ███████ ███████  ██████  ',self._logger,'i')
        ET.autolog(f'##############################################',self._logger,'i')
        ET.autolog(f'##############################################',self._logger,'i')
        ET.autolog(f'##############################################',self._logger,'i')
        ET.autolog(f'-----Python: {sys.version}--------',self._logger,'i')
        ET.autolog(f'-----OS: {os.system("uname -a")}--------',self._logger,'i')
        ET.autolog(f'-----Platform: {platform.version()}--------',self._logger,'i')
        ET.autolog(f'-----Who: {pwd.getpwuid(os.geteuid())[0]}--------',self._logger,'i')
        ET.autolog(f'##STARTNG A FRESH {self._analysisname} ANALYSIS on ## {dt_string} ##',self._logger,'i')
        ET.autolog(f'####-----------------------------------####',self._logger,'i')
        ET.autolog(f'##############################################',self._logger,'i')
        ET.autolog(f'##############################################',self._logger,'i')
        ET.autolog(f'##############################################',self._logger,'i')
        ET.autolog(f'Inside process',self._logger,'i')
        #------- Initialize accumulator with histograms
        try:
            out = self.accumulator.identity()
        except Exception:
            ET.autolog(f'Can not create accumulator of histograms',self._logger,'e')
            ET.autolog(traceback.print_exc(),self._logger,'e')
            
        #------- preprocess (mostly create objects and special event variables)
        startevents=len(events)
        out['events_processed'].fill(events_processed=np.ones(len(events)))
        out['sumw'].fill(sumw=np.ones(len(events)))
        
        try:
            events,dataset,isData,histAxisName,year,xsec,sow=self._preprocess(self._samples,events)
            eventsafterpreprocessing=len(events)
            ET.autolog(f'{len(events)} Events after preprocessing',self._logger,'i')
        except Exception:
            ET.autolog(f'Can not preprocess',self._logger,'e')
            ET.autolog(traceback.print_exc(),self._logger,'e')
        #------- preselect and store cutflow
        try:
            events,out=self._preselect(isData,events,out)
            eventsafterpreselection=len(events)
            ET.autolog(f'{len(events)} Events after preselection',self._logger,'i')
        except Exception:
            ET.autolog(f'Can not preselect',self._logger,'e')
            ET.autolog(traceback.print_exc(),self._logger,'e')
        #------- run analysis
        self._summary(self._summarylog,f'sub-job_{threadn} {startevents} {eventsafterpreprocessing} {eventsafterpreselection}',lastline=True)
        try:
            filename=self._varstosave(threadn,self._logger,events,histAxisName,self._outfolder+'/trees/')
            ET.autolog(f'{len(events)} Events after saving to root (Ignore if saveRoot was off)',self._logger,'i')
        except Exception:
            ET.autolog(f'Can not save root file',self._logger,'e')
            ET.autolog(traceback.print_exc(),self._logger,'e')
            
        try:
            out = self._analysis(self._logger,out,events,dataset,isData,histAxisName,year,xsec,sow)
            ET.autolog(f'{len(events)} Events after full analysis to root',self._logger,'i')
        except Exception:
            ET.autolog(f'Can not analyze',self._logger,'e')
            ET.autolog(traceback.print_exc(),self._logger,'e')
        #------- return accumulator
        sys.stdout.close()
        sys.stderr.close()
        return out

    def postprocess(self, accumulator):

        
        #Job Summary
        for substring in ['error','stderr','warning']:
            logdirerr='Analysis/'+self._analysisname+'/log/*/*'+substring+'*'
            for f in glob.glob(logdirerr):
                #print(f)
                jobname=os.path.basename(os.path.dirname(f))
                #f = os.path.join(logdir, filename)
                # checking if it is a file
                if os.path.isfile(f):
                    if os.stat(f).st_size != 0:
                        print(f'{jobname} has some {substring}, check logfile_{substring} file!')

        return accumulator
