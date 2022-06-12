from coffea.analysis_tools import PackedSelection
import awkward as ak
from modules.ecuts import cutflow
from modules.paths import IHEP_path
from coffea.lumi_tools import LumiMask

def preselection(year,isData,events,out):

    if year == "2016" or year == "2016APV":
        golden_json_path = IHEP_path("data/goldenJsons/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt")
    elif year == "2017":
        golden_json_path = IHEP_path("data/goldenJsons/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt")
    elif year == "2018":
        golden_json_path = IHEP_path("data/goldenJsons/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt")
    else:
        raise ValueError(f"Error: Unknown year \"{year}\".")
    lumi_mask = LumiMask(golden_json_path)(events.run,events.luminosityBlock)

    #-----------Add your pre selection here----------------------#
    #-------------------------------------------------------------
    selections = PackedSelection(dtype='uint64')

    if isData: selections.add("is_good_lumi",lumi_mask)

    selections.add("leadingelectronpt>5",ak.pad_none(events.Electron,1).pt[:,0] > 0)
    
    
    #selections.add("sub-leadingelectronpt>10",ak.pad_none(events.Electron,2).pt[:,1] > 10)
    #-------------------------------------------------------------
    out=cutflow(out,events,selections,cumulative=True,printit=False)
    return events[selections.all(*selections.names)],out
    #-------------------------------------------------------------
    
    



