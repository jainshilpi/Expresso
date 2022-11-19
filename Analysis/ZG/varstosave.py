import awkward as ak
import modules.ExpressoTools as ET

def varstosave(threadn,logger,events,filename='sample',outputfolder='./'):
    ###########################################################
    varslist= {
        "event":events['event'],
        "leading_leptonpt": ak.pad_none(events.lightlepton,1).pt[:,0],
        "leading_leptoneta":ak.pad_none(events.lightlepton,1).eta[:,0],
        "leading_leptonphi":ak.pad_none(events.lightlepton,1).phi[:,0],

        "leading_taupt": ak.pad_none(events.mytau,1).pt[:,0],
        "leading_taupt": ak.pad_none(events.mytau,1).eta[:,0],
        "leading_taupt": ak.pad_none(events.mytau,1).phi[:,0],

        "leading_photonpt": ak.pad_none(events.myphoton,1).pt[:,0],
        "leading_photonpt": ak.pad_none(events.myphoton,1).eta[:,0],
        "leading_photonpt": ak.pad_none(events.myphoton,1).phi[:,0],

        "Missing_ET": events.MET.pt,
        "dr_lg":events.drlg1,
        "dr_lt": events.drlt,
        "dr_gt": events.drgt,
        "dphi_lg": events.dphilg,
        "dphi_gt": events.dphigt,
        "dphi_lt": events.dphilt,
        "invarmass": events.invarmass
    }
    ###########################################################
    filename=ET.saveroot(threadn,logger,varslist,filename,outputfolder)
    return filename,events
