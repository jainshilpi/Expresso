import awkward as ak
from modules.paths import IHEP_path,golden_json_path
from coffea.lumi_tools import LumiMask

def preselection(pars,events,selections):
    year,isData,analysispoint=pars['year'],pars['isData'],pars['analysispoint']
    #-----------Add your pre selection here----------------------#
    if isData:
        lumi_mask = LumiMask(golden_json_path(year))(events.run,events.luminosityBlock)
        selections.add("is_good_lumi",lumi_mask)
        
    selections.add("atleast two electrons",(ak.num(events.ele)==2))
    selections.add("leading electron pt>10",(ak.pad_none(events.ele,1).pt[:,0] > 10))
    selections.add("sub-leading electron pt>7",(ak.pad_none(events.ele,2).pt[:,1] > 7))    

    return events,selections


