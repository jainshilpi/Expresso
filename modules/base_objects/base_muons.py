from modules.corrections import SFevaluator, GetBTagSF, ApplyJetCorrections, GetBtagEff, AttachMuonSF, AttachElectronSF, AttachPerLeptonFR, GetPUSF, ApplyRochesterCorrections, ApplyJetSystematics, AttachPSWeights, AttachPdfWeights, AttachScaleWeights, GetTriggerSF
from modules.selection import *
from modules.objects import *
import modules.ExpressoTools as ET

def base_muons(mu,year,AttachSF,isData):
    if AttachSF: AttachMuonSF(mu,year=year)

    mu["conept"] = coneptMuon(mu.pt, mu.mvaTTH, mu.jetRelIso, mu.mediumId)
    mu["btagDeepFlavB"] = ak.fill_none(mu.matched_jet.btagDeepFlavB, -99)

    if not isData:
        mu["gen_pdgId"] = mu.matched_gen.pdgId
        mu["gen_parent_pdgId"] = mu.matched_gen.distinctParent.pdgId
        mu["gen_gparent_pdgId"] = mu.matched_gen.distinctParent.distinctParent.pdgId

    mu["isPres"] = isPresMuon(mu.dxy, mu.dz, mu.sip3d, mu.eta, mu.pt, mu.miniPFRelIso_all)
    mu["isLooseM"] = isLooseMuon(mu.miniPFRelIso_all,mu.sip3d,mu.looseId)
    mu["isFO"] = isFOMuon(mu.pt, mu.conept, mu.btagDeepFlavB, mu.mvaTTH, mu.jetRelIso, year)
    mu["isTightLep"]= tightSelMuon(mu.isFO, mu.mediumId, mu.mvaTTH)

    mu_loose= mu[mu.isPres & mu.isLooseM]
    mu_loose=ET.sortconept(mu_loose)

    mu_fo = mu[mu.isPres & mu.isLooseM & mu.isFO]
    mu_fo=ET.sortconept(mu_fo)

    return mu_loose,mu_fo

