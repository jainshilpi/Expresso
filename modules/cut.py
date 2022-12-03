import modules.cut_configure as cut
def ispresTau(pt, eta, dxy, dz, idDeepTau2017v2p1VSjet, minpt=20.0):
    return  (pt>minpt)&(abs(eta)< cut.eta_tau_cut )&(abs(dxy)<cut.dxy_tau_cut)&(abs(dz)<cut.dz_tau_cut) & (idDeepTau2017v2p1VSjet>>1 & 1 ==1)

def istightTau(idDeepTau2017v2p1VSjet):
    return (idDeepTau2017v2p1VSjet>>2 & 1 ==1)

def ismedTau(idDeepTau2017v2p1VSjet):
    return (idDeepTau2017v2p1VSjet>>2 & 1 ==1)

def islooseTau(idDeepTau2017v2p1VSjet):
    return (idDeepTau2017v2p1VSjet>>2 & 1 ==1)

def istightElectron(pt,eta,cutBased, minpt=24.0):
    return (pt>minpt) & (abs(eta)<cut.eta_electron_cut) & (cutBased >= 4)

def ismedElectron(pt,eta,cutBased, minpt=24.0):
    return (pt>minpt) & (abs(eta)<cut.eta_electron_cut) & (cutBased >= 3)

def islooseElectron(pt,eta,cutBased, minpt=24.0):
    return (pt>minpt) & (abs(eta)<cut.eta_electron_cut) & (cutBased >= 2)

def istightMuon(pt,eta,cutBased, minpt=20.0):
    return (pt>minpt) & (abs(eta)<cut.eta_muon_cut) & (cutBased ==True)

def ismedMuon(pt,eta,cutBased, minpt=20.0):
    return (pt>minpt) & (abs(eta)<cut.eta_muon_cut) & (cutBased ==True)

def islooseMuon(pt,eta,cutBased, minpt=20.0):
    return (pt>minpt) & (abs(eta)<cut.eta_muon_cut) & (cutBased ==True)

def istightPhoton(pt,eta,cutBased, minpt=5):
    return (pt>minpt) & (abs(eta)<cut.eta_photon_cut) & (cutBased >= 3)

def ismedPhoton(pt,eta,cutBased, minpt=5):
    return (pt>minpt) & (abs(eta)<cut.eta_photon_cut) & (cutBased >= 2)

def isloosePhoton(pt,eta,cutBased, minpt=5):
    return (pt>minpt) & (abs(eta)<cut.eta_photon_cut) & (cutBased >= 1)

def isClean(obj_A, obj_B, drmin=0.4):
    objB_near, objB_DR = obj_A.nearest(obj_B, return_metric=True)
    mask = ak.fill_none(objB_DR > drmin, True)
    return (mask)
