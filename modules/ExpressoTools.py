import awkward as ak
import yaml
import cloudpickle
import gzip
import os
import pickle
import ctypes
# System dependent, see e.g. /usr/include/x86_64-linux-gnu/asm/unistd_64.h
libc,SYS_gettid = ctypes.cdll.LoadLibrary('libc.so.6'),186

'''---------------------------------------------------------------------------'''
def in_range_mask(in_var,lo_lim=None,hi_lim=None):
        if (lo_lim is None) and (hi_lim is None):
            raise Exception("Error: No cuts specified")
        if lo_lim is not None:
            above_min = (in_var > lo_lim)
        else:
            above_min = (ak.ones_like(in_var)==1)
        if hi_lim is not None:
            below_max = (in_var <= hi_lim)
        else:
            below_max = (ak.ones_like(in_var)==1)
        return ak.fill_none((above_min & below_max),False)
'''---------------------------------------------------------------------------'''
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
    elif level=='w':
        logger.warning(message)
    else:
        print(message)
'''---------------------------------------------------------------------------'''
#----------------------------------------------------------------------

def saveroot(threadn,logger,varslist,filename='sample',outputfolder='./'):
    import ROOT
    import glob

    #import logging
    #logger = logging.getLogger(__name__)
    #logger.error("saving root file")
    autolog("saving root file",logger)

    os.system(f'mkdir -p {outputfolder}/{filename}/')
    outputfolder=outputfolder+'/'+filename+'/'
    for key in varslist.keys():
        varslist[key]=ak.to_numpy(ak.fill_none(varslist[key],-9999))
    df = ROOT.RDF.MakeNumpyDataFrame(varslist)
    countsame=0
    for f_name in os.listdir(outputfolder):
            if f_name.startswith(filename+'_sub-job_'+str(threadn)) and f_name.endswith('.root'):
                    countsame=countsame+1
    filename=outputfolder+'/'+filename+'_sub-job_'+str(threadn)+"_"+str(countsame)
    df.Snapshot("Events",filename+'.root')
    return filename

#--------------------------------------------------------------------- Sorter by conept
def sortconept(obj):
    obj[ak.argsort(obj.conept, axis=-1,ascending=False)]
    return obj
#---------------------------------------------------------------------
def sortpt(obj):
    obj[ak.argsort(obj.pt, axis=-1,ascending=False)]
    return obj


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
    nEvents                = samples["nEvents"]
    return dataset,isData,histAxisName,year,xsec,sow
