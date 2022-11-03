import awkward as ak
import modules.ExpressoTools as ET

def varstosave(threadn,logger,events,filename='sample',outputfolder='./'):
    ###########################################################
    varslist= {
        "event":events['event'],
        "leading_electronpt": ak.pad_none(events.myelectron,1).pt,
        "leading_electroneta":ak.pad_none(events.myelectron,1).eta,
        "leading_muonpt": ak.pad_none(events.mymuon,1).pt,
        "leading_taupt": ak.pad_none(events.mytau,1).pt,
        "leading_photonpt": ak.pad_none(events.myphoton,1).pt
    }
    ###########################################################
    filename=ET.saveroot(threadn,logger,varslist,filename,outputfolder)
    return filename,events
