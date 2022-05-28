import awkward as ak
import modules.ExpressoTools as ET

def varstosave(logger,events,filename='sample',outputfolder='./'):
    ###########################################################
    varslist= {
        "event":events['event'],
        "run":events['run'],
        "leading_elept": ak.pad_none(events.Electron,1).pt[:,0],
        "leading_mupt": ak.pad_none(events.Muon,1).pt[:,0],
        "leading_jetpt": ak.pad_none(events.Jet,1).pt[:,0]
    }
    ###########################################################
    filename=ET.saveroot(logger,varslist,filename,outputfolder)
    return filename
