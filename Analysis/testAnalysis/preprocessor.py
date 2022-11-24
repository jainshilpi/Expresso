def preprocess(pars,ev,AttachSF=True):
    
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
    dataset,isData,histAxisName,year,xsec,sow=pars['dataset'],pars['isData'],pars['histAxisName'],pars['year'],pars['xsec'],pars['sow']
    ###################################
    #--------------------------------------------------------------------- Electrons
    ev["ele_loose"],ev["ele_fo"]=base_electrons(ev.Electron,year,AttachSF,isData)
    #--------------------------------------------------------------------- Muons
    ev["mu_loose"],ev["mu_fo"]=base_muons(ev.Muon,year,AttachSF,isData)
    #--------------------------------------------------------------------- leptons
    ev["lep_loose"],ev["lep_fo"]=base_leptons(ev["ele_loose"],ev["mu_loose"],ev["ele_fo"],ev["mu_fo"])
    #--------------------------------------------------------------------- JETMET
    ev["goodJets"] = base_jets(ev.Jet,ev["lep_fo"])
    ev["met"]  = base_met(ev.MET)
    #--------------------------------------------------------------------- Min invariant mass
    # Compute pair invariant masses, for all flavors all signes
    llpairs = ak.combinations(ev["lep_loose"], 2, fields=["l0","l1"])
    ev["minMllAFAS"] = ak.min( (llpairs.l0+llpairs.l1).mass, axis=-1)

    return ev
