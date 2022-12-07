import awkward as ak
from modules.paths import IHEP_path,golden_json_path
from coffea.lumi_tools import LumiMask

def preselection(pars, events, selections):
    #-----------Add your pre selection here----------------------#
    year,isData,analysispoint=pars['year'],pars['isData'],pars['analysispoint']
    if isData:
        lumi_mask = LumiMask(golden_json_path(year))(events.run,events.luminosityBlock)
        selections.add("is_good_lumi",lumi_mask)

    selections.add("at least 2 gen taus/eles/mus", (ak.num(events.GenTaus) > 1) | (ak.num(events.GenEles) > 1) | (ak.num(events.GenMuons) > 1) )    

    #-----------Add your pre selection here----------------------#
    return events, selections


