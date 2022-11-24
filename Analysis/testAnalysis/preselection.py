import awkward as ak
from modules.paths import IHEP_path,golden_json_path
from coffea.lumi_tools import LumiMask

def preselection(pars,events,selections):
    #-----------Add your pre selection here----------------------#
    year,isData,analysispoint=pars['year'],pars['isData'],pars['analysispoint']
    
    if isData:
        lumi_mask = LumiMask(golden_json_path(year))(events.run,events.luminosityBlock)
        selections.add("is_good_lumi",lumi_mask)

    selections.add("leading electron pt>7",ak.pad_none(events.Electron,1).pt[:,0] > 7)
    selections.add("sub-leading electron pt>7",ak.pad_none(events.Electron,2).pt[:,1] > 7)
    if 'tight' in analysispoint:
        selections.add("sub-leading electron pt>20",ak.pad_none(events.Electron,2).pt[:,1] > 20)
    #selections.add("at least two jet",ak.num(events.Jet)==2)
    #selections.add("at least one jet",ak.num(events.Jet)>=1)
    

    return events,selections


