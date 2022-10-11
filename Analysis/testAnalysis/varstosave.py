import awkward as ak
import modules.ExpressoTools as ET

def varstosave(threadn,logger,events,filename='sample',outputfolder='./'):
    ###########################################################
    varslist= {
        "event":events['event'],
        "run":events['run'],
        "leading_elept": ak.pad_none(events.Electron,1).pt[:,0],
        #"elept3": events[ak.num(events.Electron)>2].Electron.pt[:,2],
        "leading_mupt": ak.pad_none(events.Muon,1).pt[:,0],
        "leading_jetpt": ak.pad_none(events.Jet,1).pt[:,0]
    }
    ###########################################################
    filename=ET.saveroot(threadn,logger,varslist,filename,outputfolder)
    return filename,events
