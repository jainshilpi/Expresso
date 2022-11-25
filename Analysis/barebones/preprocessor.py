def preprocess(pars,ev,AttachSF=True):
    
    import awkward as ak    
    import modules.ExpressoTools as ET
    import modules.cut as cut

    ###################################
    dataset,isData,histAxisName,year=pars['dataset'],pars['isData'],pars['histAxisName'],pars['year']
    analysispoint=pars['analysispoint']
    xsec,sow,pass_options=pars['xsec'],pars['sow'],pars['passoptions']    
    ###################################

    ev["Electron","istight"]=cut.istightElectron(ev.Electron.pt, ev.Electron.eta, ev.Electron.cutBased, 24)
    ev["Electron","ismed"]=cut.ismedElectron(ev.Electron.pt, ev.Electron.eta, ev.Electron.cutBased, 24)
    ev["Electron","isloose"]=cut.islooseElectron(ev.Electron.pt, ev.Electron.eta, ev.Electron.cutBased, 24)

    ev["Muon","istight"]=cut.istightMuon(ev.Muon.pt, ev.Muon.eta, ev.Muon.tightId, 20)
    ev["Muon","ismed"]=cut.ismedMuon(ev.Muon.pt, ev.Muon.eta, ev.Muon.mediumId, 20)
    ev["Muon","isloose"]=cut.islooseMuon(ev.Muon.pt, ev.Muon.eta, ev.Muon.looseId, 20)

    ev["Photon","istight"]=cut.istightPhoton(ev.Photon.pt, ev.Photon.eta, ev.Photon.cutBased, 5)
    ev["Photon","ismed"]=cut.ismedPhoton(ev.Photon.pt, ev.Photon.eta, ev.Photon.cutBased, 5)
    ev["Photon","isloose"]=cut.isloosePhoton(ev.Photon.pt, ev.Photon.eta, ev.Photon.cutBased, 5)
    #--------------------------------------------------------------------- Electrons

    if 'tight_ele' in analysispoint:
        ev['ele']=ev.Electron[ev["Electron","istight"]]
    elif 'loose_ele' in analysispoint:
        ev['ele']=ev.Electron[ev["Electron","isloose"]]
    elif 'med_ele' in analysispoint:
        ev['ele']=ev.Electron[ev["Electron","ismed"]]
    else:
        ev['ele']=ev.Electron
    ev['Nele']=ak.num(ev.ele)

    
    if 'tight_mu' in analysispoint:
        ev['mu']=ev.Muon[ev["Muon","istight"]]
    elif 'loose_mu' in analysispoint:
        ev['mu']=ev.Muon[ev["Muon","isloose"]]
    elif 'med_mu' in analysispoint:
        ev['mu']=ev.Muon[ev["Muon","ismed"]]
    else:
        ev['mu']=ev.Muon
    ev['Nmu']=ak.num(ev.mu)
    ##-------------------------------------------------------------------------------------    
    return ev
