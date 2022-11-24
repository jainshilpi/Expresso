import awkward as ak, coffea, copy
from coffea import hist, analysis_tools
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
from coffea.analysis_tools import PackedSelection
import numpy.ma as ma
import numpy as np
from modules.hcoll import binning

histograms = {
    'ElectronPt':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('ElectronPt', '$E$P_t(GeV)', binning(20,100,10))),
    'ElectronPt':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('ElectronPt', '$E$P_t(GeV)', binning(20,100,10))),
    'MuonPt':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('MuonPt', '$Mu$P_t(GeV)', binning(20,100,10))),
    'TauPt_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('TauPt_eh', '$Tau$P_teh(GeV)', binning(30,100,10))),
    'TauPt_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('TauPt_uh', '$Tau$P_tuh(GeV)', binning(30,100,10))),

    'Electroneta':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Electroneta', '$Electroneta$', binning(-4,4,0.1))),
    'Muoneta':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Muoneta', '$Muoneta$', binning(-4,4,0.1))),
    'Taueta_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Taueta_eh', '$Taueta_eh$', binning(-4,4,0.1))),
    'Taueta_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Taueta_uh', '$Taueta_uh$', binning(-4,4,0.1))),

    'Electronphi':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Electronphi', '$Electronphi$', binning(-4,4,0.1))),
    'Muonphi':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Muonphi', '$Muonphi$', binning(-4,4,0.1))),
    'Tauphi_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Tauphi_eh', '$Tauphi_eh$', binning(-4,4,0.1))),
    'Tauphi_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Tauphi_uh', '$Tauphi_uh$', binning(-4,4,0.1))),

    'drlt_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('drlt_eh', '$drlt_eh$', binning(0,10,0.1))),
    'drlt_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('drlt_uh', '$drlt_uh$', binning(0,10,0.1))),

    'drgt_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('drgt_eh', '$drgt_eh$', binning(0,10,0.1))),
    'drgt_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('drgt_uh', '$drgt_uh$', binning(0,10,0.1))),

    'drlg_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('drlg_eh', '$drlg_eh$', binning(0,10,0.1))),
    'drlg_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('drlg_uh', '$drlg_uh$', binning(0,10,0.1))),

    'dphilg_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('dphilg_eh', '$dphilg_eh$', binning(-4,4,0.1))),
    'dphilg_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('dphilg_uh', '$dphilg_uh$', binning(-4,4,0.1))),

    'dphilt_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('dphilt_eh', '$dphilt_eh$', binning(-4,4,0.1))),
    'dphilt_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('dphilt_uh', '$dphilt_uh$', binning(-4,4,0.1))),

    'dphigt_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('dphigt_eh', '$dphigt_eh$', binning(-4,4,0.1))),
    'dphigt_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('dphigt_uh', '$dphigt_uh$', binning(-4,4,0.1))),

    'invarmass_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('invarmass_eh', '$invarmass_eh$', binning(0,70,1))),
    'invarmass_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('invarmass_uh', '$invarmass_uh$', binning(0,70,1))),

    'MET':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('MET', '$MET$', binning(0,100,1))),

    'PhotonPt_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('PhotonPt_eh', '$PhotonP_teh(GeV)$', binning(4,50,1))),
    'Photoneta_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Photoneta_eh', '$Photoneta_eh$', binning(-4,4,0.1))),
    'Photonphi_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Photonphi_eh', '$Photonphi_eh$', binning(-4,4,0.1))),

    'PhotonPt_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('PhotonPt_uh', '$PhotonPt_uh(GeV)$', binning(4,50,0.1))),
    'Photoneta_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Photoneta_uh', '$Photoneta_uh$', binning(-4,4,0.1))),
    'Photonphi_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Photonphi_uh', '$Photonphi_uh$', binning(-4,4,0.1)))
}


def myanalysis(pars,logger, h, ev, doweight=True):
    dataset,isData,histAxisName,year=pars['dataset'],pars['isData'],pars['histAxisName'],pars['year']
    xsec,sow,pass_options,analysis_point=pars['xsec'],pars['sow'],pars['passoptions'],pars['analysispoint']
    from modules.hcoll import hcoll,binning
    hists = hcoll(h, isData, xsec, sow, doweight, process=histAxisName)
    ET.autolog(f"{len(ev)} Events at the start of your analysis", logger, 'i')
    # Start your analysis``
    #-------------------------------------------------------------------------------------------------------
    # Create any needed branches
    #-------------------------------------------------------------------------------------------------------
    # Define pass options
    #-------------------------------------------------------------------------------------------------------
    # For MC
    if not isData:
         if 'Xsecweight' in pass_options:
            genw = ev["genWeight"]
            ev["weight_norm"] = (xsec / sow) * genw
         else:
            ev["weight_norm"]=1
    #-------------------------------------------------------------------------------------------------------
    # Masks
    #-------------------------------------------------------------------------------------------------------
    #Dilepton events
    #-------------------------------------------------------------------------------------------------------
    #Special masks
    #-------------------------------------------------------------------------------------------------------
    if 'tight_photon' in analysis_point:
        ev["mytau"]=ev.Tau[ev.Tau.istight]
        ev["myphoton"]=ev.Photon[ev.Photon.istight]
    # Fill histograms 
    
    hists.fill('ElectronPt',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.l[:,0], ElectronPt='pt')
    hists.fill('Electroneta',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.l[:,0], Electroneta='eta')
    hists.fill('Electronphi',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.l[:,0], Electronphi='phi')

    hists.fill('MuonPt',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.l[:,0], MuonPt='pt')
    hists.fill('Muoneta',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.l[:,0], Muoneta='eta')
    hists.fill('Muonphi',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.l[:,0], Muonphi='phi')

    hists.fill('TauPt_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.mytau[:,0], TauPt_eh='pt')
    hists.fill('Taueta_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.mytau[:,0], Taueta_eh='eta')
    hists.fill('Tauphi_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.mytau[:,0], Tauphi_eh='phi')

    hists.fill('TauPt_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.mytau[:,0], TauPt_uh='pt')
    hists.fill('Taueta_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.mytau[:,0], Taueta_uh='eta')
    hists.fill('Tauphi_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.mytau[:,0], Tauphi_uh='phi')

    hists.fill('PhotonPt_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.myphoton[:,0], PhotonPt_eh='pt')
    hists.fill('Photoneta_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.myphoton[:,0], Photoneta_eh='eta')
    hists.fill('Photonphi_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev.myphoton[:,0], Photonphi_eh='phi')

    hists.fill('PhotonPt_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.myphoton[:,0], PhotonPt_uh='pt')
    hists.fill('Photoneta_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.myphoton[:,0], Photoneta_uh='eta')
    hists.fill('Photonphi_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev.myphoton[:,0], Photonphi_uh='phi')

    #hists.fill('drlt_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev, drlt_eh='drlt')
    #hists.fill('drlt_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev, drlt_uh='drlt')

    # hists.fill('drgt_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev, drgt_eh='drgt')
    # hists.fill('drgt_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev, drgt_uh='drgt')

    # hists.fill('drlg_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev, drlg_eh='drlg1')
    # hists.fill('drlg_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev, drlg_uh='drlg1')

    # hists.fill('dphilg_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev, dphilg_eh='dphilg')
    # hists.fill('dphilg_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev, dphilg_uh='dphilg')

    # hists.fill('dphilt_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev, dphilt_eh='dphilt')
    # hists.fill('dphilt_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev, dphilt_uh='dphilt')

    # hists.fill('dphigt_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev, dphigt_eh='dphigt')
    # hists.fill('dphigt_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev, dphigt_uh='dphigt')


    # hists.fill('invarmass_eh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==11), ev, invarmass_eh='invarmass')
    # hists.fill('invarmass_uh',ev.weight_norm, (abs(ev.l[:,0].pdgId) ==13), ev, invarmass_uh='invarmass')
    hists.fill('MET',ev.weight_norm, ((abs(ev.l[:,0].pdgId) ==13)|(abs(ev.l[:,0].pdgId) ==11)),ev.MET, MET='pt')
    #-------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------
    #End your analysis
    #-------------------------------------------------------------------------------------------------------
    ET.autolog(f"{len(ev)} Events at the end of your analysis", logger, 'i')
    return hists.get()
