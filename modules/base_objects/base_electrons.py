from modules.corrections import SFevaluator, GetBTagSF, ApplyJetCorrections, GetBtagEff, AttachMuonSF, AttachElectronSF, AttachPerLeptonFR, GetPUSF, ApplyRochesterCorrections, ApplyJetSystematics, AttachPSWeights, AttachPdfWeights, AttachScaleWeights, GetTriggerSF
from modules.selection import *
from modules.objects import *
import modules.ExpressoTools as ET
import awkward as ak

def base_electrons(ele,year,AttachSF,isData):

    if AttachSF: AttachElectronSF(ele,year=year)

    ele["idEmu"] = ttH_idEmu_cuts_E3(ele.hoe, ele.eta, ele.deltaEtaSC, ele.eInvMinusPInv, ele.sieie)
    ele["conept"] = coneptElec(ele.pt, ele.mvaTTH, ele.jetRelIso)
    ele["btagDeepFlavB"] = ak.fill_none(ele.matched_jet.btagDeepFlavB, -99)

    if not isData:
        ele["gen_pdgId"] = ele.matched_gen.pdgId
        ele["gen_parent_pdgId"] = ele.matched_gen.distinctParent.pdgId
        ele["gen_gparent_pdgId"] = ele.matched_gen.distinctParent.distinctParent.pdgId

    ele["isPres"] = isPresElec(ele.pt, ele.eta, ele.dxy, ele.dz, ele.miniPFRelIso_all, ele.sip3d, getattr(ele,"mvaFall17V2noIso_WPL"))
    ele["isLooseE"] = isLooseElec(ele.miniPFRelIso_all,ele.sip3d,ele.lostHits)
    ele["isFO"] = isFOElec(ele.conept, ele.btagDeepFlavB, ele.idEmu, ele.convVeto, ele.lostHits, ele.mvaTTH, ele.jetRelIso, ele.mvaFall17V2noIso_WP80, year)
    ele["isTightLep"] = tightSelElec(ele.isFO, ele.mvaTTH)

    ele_loose = ele[ele.isPres & ele.isLooseE]
    ele_loose=ET.sortconept(ele_loose)

    ele_fo = ele[ele.isPres & ele.isLooseE & ele.isFO]
    ele_fo=ET.sortconept(ele_fo)

    return ele_loose,ele_fo
