from coffea import processor
from coffea.analysis_tools import PackedSelection
from modules.ecuts import cutflow
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import hist
import threading
#import modules.ExpressoTools as ET
import traceback
import ctypes
libc = ctypes.cdll.LoadLibrary('libc.so.6')
SYS_gettid = 186
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from datetime import datetime
import pwd
import platform
import sys
import glob
import awkward as ak
import numpy as np
import logging
def reset_logging():
    manager = logging.root.manager
    manager.disabled = logging.NOTSET
    for logger in manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            logger.setLevel(logging.NOTSET)
            logger.propagate = True
            logger.disabled = False
            logger.filters.clear()
            handlers = logger.handlers.copy()
            for handler in handlers:
                # Copied from `logging.shutdown`.
                try:
                    handler.acquire()
                    handler.flush()
                    handler.close()
                except (OSError, ValueError):
                    pass
                finally:
                    handler.release()
                logger.removeHandler(handler)

class IHEPProcessor(processor.ProcessorABC):
    def __init__(self,outfolder,dt,ET,loglevel,analysisname,varstosave,preprocess,preselect,analysis,histos,samples,saveroot,passoptions,extraselection):
        histos['sumw']=hist.Hist(axes=[hist.Bin("sumw", "sumw", 10, 0, 10)],
                                 label="sumw")
        histos['cutflow']=hist.Hist(axes=[hist.Cat("selection", "selection","placement"),
                                          hist.Bin("x", "x coordinate [m]", 80, 0, 80)],
                                    label="Cutflow")
        histos['cutflow_individual']=hist.Hist(axes=[hist.Cat("selection", "selection","placement"),
                                          hist.Bin("x", "x coordinate [m]", 80, 0, 80)],
                                    label="Cutflow_individual")
        histos['events_processed']=hist.Hist(axes=[hist.Bin("events_processed", "events_processed", 2, 0, 2)],label="events_processed")
        self._ET = ET
        self._accumulator = processor.dict_accumulator(histos)
        self._samples = samples
        self._analysis = analysis
        self._preprocess = preprocess
        self._preselect = preselect
        self._varstosave = varstosave
        self._analysisname = analysisname
        self._saveroot = saveroot
        self._passoptions = passoptions
        self._extraselection= extraselection
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
        self._summary(self._summarylog,f'sub-job_threadn,ev_sample,ev_preprocessing,ev_preselection,ev_savingtoroot,ev_analysis',lastline=True)
        
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
        reset_logging()
        logger = logging.getLogger(__name__)
        logger.setLevel(self._loglevel)
        threadn=libc.syscall(SYS_gettid)
        # Create handlers
        logpath=self._outfolder+'/log/sub-job_'+str(threadn)+str(datetime.now().strftime("_t-%H_%M_%S"))
        if not os.path.isdir(logpath): os.makedirs(logpath)
        debug_handler = logging.FileHandler(logpath+'/logfile_debug.log',mode='w')
        info_handler = logging.FileHandler(logpath+'/logfile_info.log',mode='w')
        warning_handler = logging.FileHandler(logpath+'/logfile_warning.log',mode='w')
        error_handler = logging.FileHandler(logpath+'/logfile_error.log',mode='w')
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
        self._ET.autolog('███████ ██   ██ ██████  ██████  ███████ ███████ ███████  ██████  ',self._logger,'i')
        self._ET.autolog('██       ██ ██  ██   ██ ██   ██ ██      ██      ██      ██    ██ ',self._logger,'i')
        self._ET.autolog('█████     ███   ██████  ██████  █████   ███████ ███████ ██    ██ ',self._logger,'i')
        self._ET.autolog('██       ██ ██  ██      ██   ██ ██           ██      ██ ██    ██ ',self._logger,'i')
        self._ET.autolog('███████ ██   ██ ██      ██   ██ ███████ ███████ ███████  ██████  ',self._logger,'i')
        self._ET.autolog(f'##############################################',self._logger,'i')
        self._ET.autolog(f'##############################################',self._logger,'i')
        self._ET.autolog(f'##############################################',self._logger,'i')
        self._ET.autolog(f'-----Python: {sys.version}--------',self._logger,'i')
        #self._ET.autolog(f'-----OS: {os.system("uname -a")}--------',self._logger,'i')
        self._ET.autolog(f'-----Platform: {platform.version()}--------',self._logger,'i')
        self._ET.autolog(f'-----Who: {pwd.getpwuid(os.geteuid())[0]}--------',self._logger,'i')
        self._ET.autolog(f'##STARTNG A FRESH {self._analysisname} ANALYSIS on ## {dt_string} ##',self._logger,'i')
        self._ET.autolog(f'####-----------------------------------####',self._logger,'i')
        self._ET.autolog(f'##############################################',self._logger,'i')
        self._ET.autolog(f'##############################################',self._logger,'i')
        self._ET.autolog(f'##############################################',self._logger,'i')
        self._ET.autolog(f'Inside process',self._logger,'i')
        #------- Initialize accumulator with histograms
        try:
            out = self.accumulator.identity()
        except Exception:
            self._ET.autolog(f'Can not create accumulator of histograms',self._logger,'e')
            self._ET.autolog(traceback.print_exc(),self._logger,'e')
        
        
        #------- preprocess (mostly create objects and special event variables)
        ev_sample=len(events)
        out['events_processed'].fill(events_processed=np.ones(len(events)))
        out['sumw'].fill(sumw=np.ones(len(events)))
        try:
            events,dataset,isData,histAxisName,year,xsec,sow=self._preprocess(self._samples,events)
            ev_preprocessing=len(events)
            self._ET.autolog(f'{len(events)} Events after preprocessing',self._logger,'i')
        except Exception:
            self._ET.autolog(f'Can not preprocess',self._logger,'e')
            ev_preprocessing=0
            self._ET.autolog(traceback.print_exc(),self._logger,'e')
        
        #------- preselect and store cutflow
        try:
            selections = PackedSelection(dtype='uint64')
            events,out,selections=self._preselect(year,isData,events,out,selections)
            if self._extraselection:
                extraselection=self._extraselection.split("=")
                e_name=extraselection[0]
                e_sel=extraselection[1]
                selections.add(e_name,eval(e_sel))
            out=cutflow(out,events,selections,printit=True)
            events=events[selections.all(*selections.names)]
            ev_preselection=len(events)
            self._ET.autolog(f'{len(events)} Events after preselection',self._logger,'i')
        except Exception:
            self._ET.autolog(f'Can not preselect',self._logger,'e')
            ev_preselection=0
            self._ET.autolog(traceback.print_exc(),self._logger,'e')
        #------- run analysis

        if(self._saveroot):
            filename,events=self._varstosave(threadn,self._logger,events,histAxisName,self._outfolder+'/trees/')
            self._ET.autolog(f'{len(events)} Events after saving to root (Ignore if saveRoot was off)',self._logger,'i')
            ev_savingtoroot=len(events)
        else:
            ev_savingtoroot=0
            #self._ET.autolog(f'Can not save root file',self._logger,'e')
            #self._ET.autolog(traceback.print_exc(),self._logger,'e')

        #print(events.fields)
        try:
            out = self._analysis(self._logger,out,events,dataset,isData,histAxisName,year,xsec,sow,self._passoptions)
            ev_analysis=len(events)
            self._ET.autolog(f'{len(events)} Events after full analysis to root',self._logger,'i')
        except Exception:
            ev_analysis=0
            self._ET.autolog(f'Can not analyze',self._logger,'e')
            self._ET.autolog(traceback.print_exc(),self._logger,'e')
            
        #------- return accumulator
        self._summary(self._summarylog,f'sub-job_{threadn},{ev_sample},{ev_preprocessing},{ev_preselection},{ev_savingtoroot},{ev_analysis}',lastline=True)
        sys.stdout.close()
        sys.stderr.close()
        
        return out

    def postprocess(self, accumulator):
        
        #Job Summary
        for substring in ['error','stderr','warning']:
            logdirerr=self._outfolder+'*/*/*'+substring+'*'
            for f in glob.glob(logdirerr):
                #print(f)
                jobname=os.path.basename(os.path.dirname(f))
                #f = os.path.join(logdir, filename)
                # checking if it is a file
                if os.path.isfile(f):
                    if os.stat(f).st_size != 0:
                        print(f)
                        print(f'{jobname} has some {substring}, check logfile_{substring} file!')
        print('Find your summary log here:')
        print(f'{self._summarylog}')

        import pandas as pd
        summarydata=pd.read_csv(f'{self._summarylog}')
        summarydata.loc['Total_Events']= summarydata.sum(numeric_only=True)
        summarydata.loc['Percent_Events']= (summarydata.loc['Total_Events']*100)/summarydata['ev_sample']['Total_Events'].round(2)
        summarydata.loc['Percent_Events']= summarydata.loc['Percent_Events'].astype(float).round(2).apply(str)+'%'
        
        original_stdout = sys.stdout # Save a reference to the original standard output
        with open(f'{self._summarylog}', 'a') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print(summarydata.to_markdown())
            print("###------- C U  T F L O W (Cumulative)-------###")
            print(accumulator['cutflow'].project('selection').to_hist())
            print("###------- C U  T F L O W (Individual)-------###")
            print(accumulator['cutflow_individual'].project('selection').to_hist())
            sys.stdout = original_stdout
            
        print(summarydata.tail(2).to_markdown())

        print("###------- C U  T F L O W (Cumulative)-------###")
        print(accumulator['cutflow'].project('selection').to_hist())
        return accumulator


if __name__=='__main__':
    print("Hello, this script is not meant to be run by itself.")
