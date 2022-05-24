import awkward as ak
from modules.selection import *
from modules.objects import *

def base_jets(jets,lep_fo):
    vetos_tocleanjets = ak.with_name( lep_fo, "PtEtaPhiMCandidate")
    tmp = ak.cartesian([ak.local_index(jets.pt), vetos_tocleanjets.jetIdx], nested=True)
    cleanedJets = jets[~ak.any(tmp.slot0 == tmp.slot1, axis=-1)]
    # this line should go before *any selection*, otherwise lep.jetIdx is not aligned with the jet index
    cleanedJets["isGood"] = isTightJet(getattr(cleanedJets, "pt"), cleanedJets.eta, cleanedJets.jetId, jetPtCut=30.)
    goodJets = cleanedJets[cleanedJets.isGood]
    return goodJets
