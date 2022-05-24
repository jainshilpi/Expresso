import modules.ExpressoTools as ET
import awkward as ak

def base_leptons(ele_loose,mu_loose,ele_fo,mu_fo):
    
    lep_loose = ak.with_name(ak.concatenate([ele_loose, mu_loose], axis=1), 'PtEtaPhiMCandidate')
    lep_loose=ET.sortconept(lep_loose)

    mu_fo['convVeto'] = ak.ones_like(mu_fo.charge);
    mu_fo['lostHits'] = ak.zeros_like(mu_fo.charge);
    lep_fo = ak.with_name(ak.concatenate([ele_fo, mu_fo], axis=1), 'PtEtaPhiMCandidate')
    lep_fo=ET.sortconept(lep_fo)

    return lep_loose,lep_fo
