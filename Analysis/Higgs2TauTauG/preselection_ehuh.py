import awkward as ak
from modules.paths import IHEP_path,golden_json_path
from coffea.lumi_tools import LumiMask

def preselection(year,isData,events,out,selections):
    #-----------Add your pre selection here----------------------#

    if isData:
        lumi_mask = LumiMask(golden_json_path(year))(events.run,events.luminosityBlock)
        selections.add("is_good_lumi",lumi_mask)
    #selections.add("eh or muh or hh channel", (events.XX)
    selections.add("delta R between electron and tau should larger than 0.4", events.drlt > 0.4)
    selections.add("charge shoule be oppsite for electron and tau", events.chargeeh == -1)
    selections.add("Invarmass for e-tau should less than 60GeV", events.invarmass < 60)
    #selections.add("Mt should less than 30GeV", events.Mteh < 30)
    #selections.add("leading electron pt>7",ak.pad_none(events.Electron,1).pt[:,0] > 7)
    #selections.add("sub-leading electron pt>7",ak.pad_none(events.Electron,2).pt[:,1] > 7)
    #selections.add("leading tau pt>10",ak.pad_none(events.Tau,1).pt[:,0] > 10)
    #selections.add("at least two jet",ak.num(events.Jet)==2)
    #selections.add("at least one jet",ak.num(events.Jet)>=1)
    

    return events,out,selections


