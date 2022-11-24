import awkward as ak
from modules.paths import IHEP_path,golden_json_path
from coffea.lumi_tools import LumiMask

def preselection(year,isData,events,out,selections):
    #-----------Add your pre selection here----------------------#

    if isData:
        lumi_mask = LumiMask(golden_json_path(year))(events.run,events.luminosityBlock)
        selections.add("is_good_lumi",lumi_mask)

    selections.add("delta R between electron and tau should larger than 0.4", events.drlt > 0.4)
    #selections.add("delta R between photon and tau should larger than 0.4", events.drgt > 0.4)
    selections.add("charge shoule be oppsite for electron and tau", events.chargeeh == -1)
    selections.add("Invarmass for e-tau should less than 60GeV", events.invarmass < 60)

    return events,out,selections


