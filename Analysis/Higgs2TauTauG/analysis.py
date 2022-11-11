import awkward as ak, coffea, copy
from coffea import hist, analysis_tools
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
from coffea.analysis_tools import PackedSelection
import numpy.ma as ma
import numpy as np

class hcoll:

    def __init__(self, h, isData, xsec, sow, doweight, **conf):
        self.h = h
        self.conf = conf
        self.isData = isData
        self.xsec = xsec
        self.sow = sow
        self.doweight=doweight

    def fill(self, name, weights, mask, obj, cat={}, flatten=False, **axes):
        fullhist = {}
        #print('----------########---')
        for ini, axis in enumerate(axes.keys()):
            arrr = eval(f"obj.{axes[axis]}[mask]")
            if flatten:
                if ini==0:
                    fullhist[axis],weights = ak.flatten(ak.zip(arrr,weights))
                    weights=weights[ak.flatten(mask)]
                else:
                    fullhist[axis] = ak.flatten(arrr)
            else:
                if ini==0:
                    weights=weights[mask]
                fullhist[axis] = arrr
        if self.doweight:
            self.h[name].fill(weight=weights, **cat, **fullhist, **self.conf)
        else:
            self.h[name].fill(**cat, **fullhist, **self.conf)

    def get(self):
        return self.h


def myanalysis(logger, h, ev, dataset, isData, histAxisName, year, xsec, sow, pass_options, doweight=True):
    
    hists = hcoll(h, isData, xsec, sow, doweight, process=histAxisName)
    ET.autolog(f"{len(ev)} Events at the start of your analysis", logger, 'i')
    # Start your analysis
    #-------------------------------------------------------------------------------------------------------
    # Create any needed branches
    #-------------------------------------------------------------------------------------------------------
    # Define pass options
    #-------------------------------------------------------------------------------------------------------
    # For MC
    if not isData:
         if pass_options=='Xsecweight':
            genw = ev["genWeight"]
            ev["weight_norm"] = (xsec / sow) * genw
            #ev["weight_norm"] =1
         else:
            ev["weight_norm"]=1
    
   
    
    #-------------------------------------------------------------------------------------------------------
    # Masks
    #-------------------------------------------------------------------------------------------------------
    #Dilepton events
    #-------------------------------------------------------------------------------------------------------
    #Special masks
    #-------------------------------------------------------------------------------------------------------
    # Fill histograms
    hists.fill('ElectronPt',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.lightlepton[:,0], ElectronPt='pt')
    hists.fill('Electroneta',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.lightlepton[:,0], Electroneta='eta')
    hists.fill('Electronphi',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.lightlepton[:,0], Electronphi='phi')
    hists.fill('MuonPt',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.lightlepton[:,0], MuonPt='pt')
    hists.fill('Muoneta',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.lightlepton[:,0], Muoneta='eta')
    hists.fill('Muonphi',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.lightlepton[:,0], Muonphi='phi')
    hists.fill('TauPt_eh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.mytau[:,0], TauPt_eh='pt')
    hists.fill('Taueta_eh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.mytau[:,0], Taueta_eh='eta')
    hists.fill('Tauphi_eh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.mytau[:,0], Tauphi_eh='phi')
    hists.fill('TauPt_uh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.mytau[:,0], TauPt_uh='pt')
    hists.fill('Taueta_uh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.mytau[:,0], Taueta_uh='eta')
    hists.fill('Tauphi_uh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.mytau[:,0], Tauphi_uh='phi')

    hists.fill('PhotonPt_eh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.myphoton[:,0], PhotonPt_eh='pt')
    hists.fill('Photoneta_eh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.myphoton[:,0], Photoneta_eh='eta')
    hists.fill('Photonphi_eh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.myphoton[:,0], Photonphi_eh='phi')
    hists.fill('PhotonPt_uh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.myphoton[:,0], PhotonPt_uh='pt')
    hists.fill('Photoneta_uh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.myphoton[:,0], Photoneta_uh='eta')
    hists.fill('Photonphi_uh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev.myphoton[:,0], Photonphi_uh='phi')

    hists.fill('dr_eh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev, dr_eh='dr')
    hists.fill('dr_uh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev, dr_uh='dr')
    hists.fill('invarmass_eh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev, invarmass_eh='invarmass')
    hists.fill('invarmass_uh',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==13), ev, invarmass_uh='invarmass')
    hists.fill('MET',ev.weight_norm, ((abs(ev.lightlepton[:,0].pdgId) ==13)|(abs(ev.lightlepton[:,0].pdgId) ==11)),ev.MET, MET='pt')
    #-------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------
    #End your analysis
    #-------------------------------------------------------------------------------------------------------
    ET.autolog(f"{len(ev)} Events at the end of your analysis", logger, 'i')
    return hists.get()

def binning(a,b,c):
    return list(np.arange(a,b+c,c))
histograms = {
    'ElectronPt':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('ElectronPt', '$ElectronPt$', binning(20,100,1))),
    'MuonPt':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('MuonPt', '$MuonPt$', binning(20,100,1))),
    'TauPt_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('TauPt_eh', '$TauPt_eh$', binning(30,100,1))),
    'TauPt_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('TauPt_uh', '$TauPt_uh$', binning(30,100,1))),

    'Electroneta':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Electroneta', '$Electroneta$', binning(-4,4,1))),
    'Muoneta':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Muoneta', '$Muoneta$', binning(-4,4,1))),
    'Taueta_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Taueta_eh', '$Taueta_eh$', binning(-4,4,1))),
    'Taueta_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Taueta_uh', '$Taueta_uh$', binning(-4,4,1))),

    'Electronphi':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Electronphi', '$Electronphi$', binning(-4,4,1))),
    'Muonphi':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Muonphi', '$Muonphi$', binning(-4,4,1))),
    'Tauphi_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Tauphi_eh', '$Tauphi_eh$', binning(-4,4,1))),
    'Tauphi_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Tauphi_uh', '$Tauphi_uh$', binning(-4,4,1))),

    'dr_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('dr_eh', '$dr_eh$', binning(0,10,1))),
    'dr_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('dr_uh', '$dr_uh$', binning(0,10,1))),
    'invarmass_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('invarmass_eh', '$invarmass_eh$', binning(0,70,1))),
    'invarmass_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('invarmass_uh', '$invarmass_uh$', binning(0,70,1))),

    'MET':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('MET', '$MET$', binning(0,100,1))),
    'PhotonPt_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('PhotonPt_eh', '$PhotonPt_eh$', binning(4,50,1))),
    'Photoneta_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Photoneta_eh', '$Photoneta_eh$', binning(-4,4,1))),
    'Photonphi_eh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Photonphi_eh', '$Photonphi_eh$', binning(-4,4,1))),
    'PhotonPt_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('PhotonPt_uh', '$PhotonPt_uh$', binning(4,50,1))),
    'Photoneta_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Photoneta_uh', '$Photoneta_uh$', binning(-4,4,1))),
    'Photonphi_uh':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Photonphi_uh', '$Photonphi_uh$', binning(-4,4,1)))

}
