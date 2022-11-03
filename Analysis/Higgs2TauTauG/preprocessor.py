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
    

    ###################################
    dataset,isData,histAxisName,year,xsec,sow=ET.getInfo(events,sample)
    ###################################
    isphoton=(ev.GenPart.pdgId==22)
    ev["genphotons"]=ev.GenPart[isphoton]
    ev["halfproperphotons"]=(ev["genphotons"][abs(ev.GenPart[ev["genphotons"].genPartIdxMother].pdgId)==15])
    ev["properphotons"]=ev["halfproperphotons"][ev.halfproperphotons.status==1]
    ev["photonswithcut"]=ev.properphotons[ev.properphotons.pt>5]
    ev["tauid"]=ev.Tau.idDecayModeNewDMs==True
    ev["mediumelectron"]=ev.Electron.cutBased >=3 & 
    ev["mediummuon"]=ev.Muon.mediumId==True

    ev["mytau"]=ev.Tau[ev.tauid]
    ev["mymuon"]=ev.Muon[ev.mediummuon]
    ev["myelectron"]=ev.Electron[ev.mediumelectron]

    ev["iseh"]=(ak.num(ev.myelectron)==1) & (ak.num(ev.mytau)==1) & (ak.num(ev.mymuon)==0) & (ak.num(ev.photonswithcut)==1)
    ev["isuh"]=(ak.num(ev.myelectron)==0) & (ak.num(ev.mytau)==1) & (ak.num(ev.mymuon)==1) & (ak.num(ev.photonswithcut)==1)
    ev["ishh"]=(ak.num(ev.myelectron)==0) & (ak.num(ev.mytau)==2) & (ak.num(ev.mymuon)==0) & (ak.num(ev.photonswithcut)==1)

    eveh=ev[ev.iseh]
    evuh=ev[ev.isuh]
    evhh=ev[ev.ishh]

    taupairs = ak.combinations(ev.mytau, 2, fields=["tau0","tau1"])

    

    eveh["dreh"]=eveh.mytau.delta_r(eveh.myelectron)
    evuh["druh"]=evuh.mytau.delta_r(evuh.mymuon)
    evhh["drhh"]=taupairs.tau0.delta_r(taupairs.tau1)


    chargeeh=eveh.mytau.charge*eveh.myelectron.charge
    chargeuh=evuh.mytau.charge*evuh.mymuon.charge
    chargehh=taupairs.tau0.charge*taupairs.tau1.charge

    eveh["invmass"]=eveh.mytau+eveh.myelectron
    ehinvarmass=eveh.invmass.mass
    evuh["invmass"]=evuh.mytau+evuh.mymuon
    uhinvarmass=evuh.invmass.mass
    evhh["invmass"]=taupairs.tau0+taupairs.tau1
    hhinvarmass=evhh.invmass.mass

    eveh["iseh1"]=(ak.flatten(chargeeh < 0)) & (ak.flatten(eveh.dreh > 0.4)) & (ak.flatten(abs(ehinvarmass-90)>15))
    evuh["isuh1"]=(ak.flatten(chargeuh < 0)) & (ak.flatten(evuh.druh > 0.4)) & (ak.flatten(abs(uhinvarmass-90)>15))
    evhh["ishh1"]=(ak.flatten(chargehh < 0)) & (ak.flatten(evhh.drhh > 0.4)) & (ak.flatten(abs(hhinvarmass-90)>15))

    eveh1=eveh[eveh.iseh1]
    evuh1=evuh[evuh.isuh1]
    evhh1=evhh[evhh.ishh1]


    # Compute pair invariant masses, for all flavors all signes

    return events,dataset,isData,histAxisName,year,xsec,sow
