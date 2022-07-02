import awkward as ak
from modules.paths import IHEP_path,golden_json_path
from coffea.lumi_tools import LumiMask

def preselection(year,isData,events,out,selections):
    #-----------Add your pre selection here----------------------#

    if isData:
        lumi_mask = LumiMask(golden_json_path(year))(events.run,events.luminosityBlock)
        selections.add("is_good_lumi",lumi_mask)

    selections.add("leading electron pt>5",ak.pad_none(events.Electron,1).pt[:,0] > 5)
    selections.add("sub-leading electron pt>5",ak.pad_none(events.Electron,2).pt[:,1] > 5)

    return events,out,selections


