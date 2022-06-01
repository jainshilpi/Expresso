from coffea import processor,hist
import modules.ExpressoTools as ET
import modules.IHEPProcessor as IHEPProcessor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import json
import logging
import threading
class IHEPAnalysis:
    
    def __init__(self,name,loglevel=logging.INFO):
        self.a=0
        self.hists={}
        self.samples=[]
        self.SampleList=[]
        self.AnalysisName=name
        self.loglevel=loglevel
        import inspect, logging
        # Create a custom logger
        #logging.basicConfig(format="thread %(threadName)s:%(message)s")
        # logger = logging.getLogger(__name__)
        # logger.setLevel(loglevel)
        # # Create handlers
        # logpath='Analysis/'+self.AnalysisName+'/log'
        # if not os.path.isdir(logpath): os.mkdir(logpath)
        # debug_handler = logging.FileHandler('Analysis/'+self.AnalysisName+'/log/logfile_debug.log')
        # info_handler = logging.FileHandler('Analysis/'+self.AnalysisName+'/log/logfile_info.log')
        # warning_handler = logging.FileHandler('Analysis/'+self.AnalysisName+'/log/logfile_warning.log')
        # error_handler = logging.FileHandler('Analysis/'+self.AnalysisName+'/log/logfile_error.log')
        # debug_handler.setLevel(logging.DEBUG)
        # info_handler.setLevel(logging.INFO)
        # warning_handler.setLevel(logging.WARNING)
        # error_handler.setLevel(logging.ERROR)
        # # Create formatters and add it to handlers
        # info_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        # warning_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        # debug_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        # error_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # info_handler.setFormatter(info_format)
        # debug_handler.setFormatter(debug_format)
        # warning_handler.setFormatter(warning_format)
        # error_handler.setFormatter(error_format)
        
        # # Add handlers to the logger
        # logger.addHandler(debug_handler)
        # logger.addHandler(info_handler)
        # logger.addHandler(warning_handler)
        # logger.addHandler(error_handler)
        # self.logger=logger
        # now = datetime.now()
        # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # ET.autolog('███████ ██   ██ ██████  ██████  ███████ ███████ ███████  ██████  ',self.logger,'i')
        # ET.autolog('██       ██ ██  ██   ██ ██   ██ ██      ██      ██      ██    ██ ',self.logger,'i')
        # ET.autolog('█████     ███   ██████  ██████  █████   ███████ ███████ ██    ██ ',self.logger,'i')
        # ET.autolog('██       ██ ██  ██      ██   ██ ██           ██      ██ ██    ██ ',self.logger,'i')
        # ET.autolog('███████ ██   ██ ██      ██   ██ ███████ ███████ ███████  ██████  ',self.logger,'i')
        # ET.autolog(f'##############################################',self.logger,'i')
        # ET.autolog(f'##############################################',self.logger,'i')
        # ET.autolog(f'##############################################',self.logger,'i')
        # ET.autolog(f'-----Python: {sys.version}--------',self.logger,'i')
        # ET.autolog(f'-----OS: {os.system("uname -a")}--------',self.logger,'i')
        # ET.autolog(f'-----Platform: {platform.version()}--------',self.logger,'i')
        # ET.autolog(f'-----Who: {pwd.getpwuid(os.geteuid())[0]}--------',self.logger,'i')
        # ET.autolog(f'##STARTNG A FRESH {self.AnalysisName} ANALYSIS on ## {dt_string} ##',self.logger,'i')
        # ET.autolog(f'####-----------------------------------####',self.logger,'i')
        # ET.autolog(f'##############################################',self.logger,'i')
        # ET.autolog(f'##############################################',self.logger,'i')
        # ET.autolog(f'##############################################',self.logger,'i')
    
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
            
    def SetAnalysis(self,analysis):
        self.analysis=analysis
        #return self.logger
    
    def run(self,xrootd="root://cmsxrootd.fnal.gov//",chunksize=100,maxchunks=1,saveroot=False):
        
        for sample in self.samples:
            sample["files"]=[xrootd + file for file in sample["files"]]
            result= processor.run_uproot_job({sample["histAxisName"]:sample["files"]},sample["treeName"],
                                             IHEPProcessor.IHEPProcessor(self.loglevel,self.AnalysisName,self.varstosave,
                                                                         self.preprocess,self.preselect,self.analysis,self.hists,sample),
                                             processor.futures_executor,{"schema": NanoAODSchema, 'workers':16} ,
                                             chunksize=chunksize, maxchunks=maxchunks)
            
            
        return result
                       
                         
                          
                         
