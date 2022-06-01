import awkward as ak
import uproot
import coffea as coffea
from coffea import hist
from coffea.analysis_tools import PackedSelection
#from coffea.lumi_tools import LumiMask
uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource
import modules.Analysis as Analysis
from modules.GetValuesFromJsons import get_param
from modules.objects import *
from modules.corrections import SFevaluator, GetBTagSF, ApplyJetCorrections, GetBtagEff, AttachMuonSF, AttachElectronSF, AttachPerLeptonFR, GetPUSF, ApplyRochesterCorrections, ApplyJetSystematics, AttachPSWeights, AttachPdfWeights, AttachScaleWeights, GetTriggerSF
from modules.selection import *
from modules.paths import IHEP_path

import yaml
import cloudpickle
import gzip
import os
import pickle

import ctypes
libc = ctypes.cdll.LoadLibrary('libc.so.6')

# System dependent, see e.g. /usr/include/x86_64-linux-gnu/asm/unistd_64.h
SYS_gettid = 186

def autolog(message,logger,level="i"):

    def getThreadId():
       """Returns OS thread id - Specific to Linux"""
       return libc.syscall(SYS_gettid)
    "Automatically log the current function details."
    import inspect
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    message=f'thread {getThreadId()}, {message}: {func.co_name} in {func.co_filename}:{func.co_firstlineno}'
    if level=='i':
        logger.info(message)
    elif level=='d':
        logger.debug(message)
    elif level=='e':
        logger.error(message)
    else:
        logger.warning(message)

    
#----------------------------------------------------------------------
def saveroot(threadn,logger,varslist,filename='sample',outputfolder='./'):

    #import logging
    #logger = logging.getLogger(__name__)
    #logger.error("saving root file")
    autolog("saving root file",logger)

    os.system(f'mkdir -p {outputfolder}/{filename}/')
    outputfolder=outputfolder+'/'+filename+'/'
    import ROOT
    filename=outputfolder+'/'+filename+'_sub-job_'+str(threadn)+'.root'
    for key in varslist.keys():
        varslist[key]=ak.to_numpy(ak.fill_none(varslist[key],-9999))
    df = ROOT.RDF.MakeNumpyDataFrame(varslist)
    df.Snapshot("Events",filename)
    return filename

#--------------------------------------------------------------------- Sorter by conept
def sortconept(obj):
    obj[ak.argsort(obj.conept, axis=-1,ascending=False)]
    return obj
#---------------------------------------------------------------------


def cprint(text,c):
    

    if c=='HEADER': xx= '\033[95m'
    if c=='OKBLUE': xx= '\033[94m'
    if c=='OKCYAN': xx= '\033[96m'
    if c=='OKGREEN': xx= '\033[92m'
    if c=='WARNING': xx= '\033[93m'
    if c=='FAIL': xx= '\033[91m'
    
    if c=='BOLD': xx= '\033[1m'
    if c=='UNDERLINE': xx= '\033[4m'
    ENDC = '\033[0m'
        
    print(xx + text + ENDC)

def parse_yml(loc):
    with open(loc, 'r') as stream:
        try:
            parsed_yaml=yaml.safe_load(stream)
            #print(parsed_yaml)
            return parsed_yaml
        except yaml.YAMLError as exc:
            print(exc)
    return 0


def saveHist(result,OutputFolder,OutputName):
    out_pkl_file=OutputFolder+"/"+OutputName+".pkl.gz"
    directory=OutputFolder
    if not os.path.exists(directory):
        os.makedirs(directory)
    with gzip.open(out_pkl_file, "wb") as fout:
        cloudpickle.dump(result, fout)


# Check if the values in an array are within a given range
def in_range_mask(in_var,lo_lim=None,hi_lim=None):

    # Make sure at least one of the cuts is not none
    if (lo_lim is None) and (hi_lim is None):
        raise Exception("Error: No cuts specified")

    # Check if the value is greater than the min
    if lo_lim is not None:
        above_min = (in_var > lo_lim)
    else:
        above_min = (ak.ones_like(in_var)==1)

    # Check if the value is less than or equal to the max
    if hi_lim is not None:
        below_max = (in_var <= hi_lim)
    else:
        below_max = (ak.ones_like(in_var)==1)

    # Return the mask
    return ak.fill_none((above_min & below_max),False)

def getInfo(events,samples):
    dataset = events.metadata["dataset"]
    isData             = samples["isData"]
    histAxisName       = samples["histAxisName"]
    year               = samples["year"]
    xsec               = samples["xsec"]
    sow                = samples["nSumOfWeights"]
    return dataset,isData,histAxisName,year,xsec,sow


def get_hist_from_pkl(path_to_pkl,allow_empty=True):
        h = pickle.load( gzip.open(path_to_pkl) )
        if not allow_empty:
            h = {k:v for k,v in h.items() if v.values() != {}}
        return h

import hist
import matplotlib.pyplot as plt
import mplhep as hep

def dictprint(di):
        for key, value in di.items():
                print(key, ' : ', value)

def dictplot(histodict,outputfolder):
    
    
    for hiname in histodict.keys():
        histo=histodict[hiname]
        fig, ax = plt.subplots()
        hep.style.use('CMS')
        hep.cms.label('', data=False)
        nostack=[]
        stack=[]
        nostacklabels=[]
        stacklabels=[]
        for k in histo.keys():
            dicty=histo[k]
            scale=1.0
            if 'scale' in histo[k].keys():
                scale=histo[k]['scale']

            thist=get_hist_from_pkl(outputfolder+"/"+histo[k]['file'])[k]
            thist.scale(scale)
            #histo[k]['h']=get_hist_from_pkl(histo[k]['file'])[k].to_hist().project(histo[k]['axis'])
            histo[k]['h']=thist.to_hist().project(histo[k]['axis'])
            if(histo[k]['stack']==True):
                stack.append(histo[k]['h'])
                stacklabels.append(histo[k]['label'])
            if(histo[k]['stack']==False):
                nostack.append(histo[k]['h'])
                nostacklabels.append(histo[k]['label'])
        if len(stack)!=0:
            hep.histplot(stack,ax=ax,lw=3,stack=True,histtype='fill',label=stacklabels)
        if len(nostack)!=0:
            hep.histplot(nostack,ax=ax,lw=3,stack=False,histtype='step',label=nostacklabels, yerr=True)
        plt.legend(loc='best')
        plt.savefig(f'{outputfolder}/{hiname}.pdf', dpi=150)
