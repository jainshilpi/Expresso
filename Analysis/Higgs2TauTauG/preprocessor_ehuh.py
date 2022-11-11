from asyncio import events


def preprocess(sample,events,AttachSF=True):
    
    import awkward as ak    
    import modules.ExpressoTools as ET
    from modules.corrections import SFevaluator, GetBTagSF, ApplyJetCorrections, GetBtagEff, AttachMuonSF, AttachElectronSF, AttachPerLeptonFR, GetPUSF, ApplyRochesterCorrections, ApplyJetSystematics, AttachPSWeights, AttachPdfWeights, AttachScaleWeights, GetTriggerSF
    #from modules.selection import *
    #from modules.objects import *
    from modules.base_objects.base_electrons import base_electrons
    from modules.base_objects.base_muons import base_muons
    from modules.base_objects.base_leptons import base_leptons
    from modules.base_objects.base_jets import base_jets
    from modules.base_objects.base_met import base_met
    import numpy as np
    

    ###################################
    dataset,isData,histAxisName,year,xsec,sow=ET.getInfo(events,sample)
    ###################################
    isphoton=(events.GenPart.pdgId==22)
    events["genphotons"]=events.GenPart[isphoton]
    events["halfproperphotons"]=(events["genphotons"][abs(events.GenPart[events["genphotons"].genPartIdxMother].pdgId)==15])
    events["properphotons"]=events["halfproperphotons"][events.halfproperphotons.status==1]
    events["photonswithcut"]=events.properphotons[events.properphotons.pt>5]
    events["ttgevents"]=(ak.num(events.photonswithcut)==1)


    #events["mytau"]=events.Tau[(events.Tau.idDecayModeNewDMs==True) & (events.Tau.pt > 30) & (events.Tau.pt <45) & (abs(events.Tau.eta)<2.4)]
    events["mytau"]=events.Tau[(events.Tau.idDecayModeNewDMs==True) & (events.Tau.pt > 30) &  (abs(events.Tau.eta)<2.4)]
    events["myelectron"]=events.Electron[(events.Electron.cutBased >=3) & (events.Electron.pt > 24) & (abs(events.Electron.eta)<2.1)]
    events["myphoton"]=events.Photon[(events.Photon.cutBased >=2) & (events.Photon.pt > 5) & (abs(events.Photon.eta)<2.5)]
    events["mymuon"]=events.Muon[(events.Muon.mediumId==True) & (events.Muon.pt > 20) & (abs(events.Muon.eta)<2.1)]
    events["lightlepton"]=ak.with_name(ak.concatenate([events.myelectron, events.mymuon], axis=1), 'PtEtaPhiMCandidate')
    if histAxisName=="H2TTTG":
        events=events[(events.ttgevents==1)]
    elif histAxisName=="H2TTT":
        events=events[(events.ttgevents==0)]
    else:
        events=events
    
    events=events[ak.num(events.lightlepton)==1]
    events["drlg"]=events.myphoton.delta_r(events.lightlepton[:,0])
    events.myphoton=events.myphoton[events.drlg > 0.4]
    events=events[(ak.num(events.mytau)==1) & (ak.num(events.myphoton)==1)]

    ev_tau=events.mytau[:,0]
    ev_lepton=events.lightlepton[:,0]
    ev_photon=events.myphoton[:,0]

    events["lhobject"]=ev_tau+ev_lepton
    events["lhgobject"]=ev_tau+ev_lepton+ev_photon

    events["dr"]=ev_lepton.delta_r(ev_tau)
    events["chargeeh"]=ev_lepton.charge*ev_tau.charge
    events["invarmass"]=events.lhobject.mass
    #events["Mteh"]=np.sqrt(2*ev_lepton.pt*ev_tau.pt*(1-np.cos(ev_lepton.delta_phi(ev_tau))))
    # Compute pair invariant masses, for all flavors all signes

    return events,dataset,isData,histAxisName,year,xsec,sow
