import awkward as ak, coffea, copy
from coffea import hist, analysis_tools
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
from coffea.analysis_tools import PackedSelection
import numpy.ma as ma
import numpy as np
from modules.hcoll import binning

from asyncio import events
    ############################# KEEP THIS BLOCK ##################
histograms = {
    ############################# KEEP THIS BLOCK ##################
    
    'M_eeg':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('M_eeg', 'M_eeg(GeV)', binning(20,200,1))),
    'M_mmg':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('M_mmg', 'M_mmg(GeV)', binning(20,200,1))),
    'M_ttg':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('M_ttg', 'M_ttg(GeV)', binning(20,200,1))),

    ############################# KEEP THIS BLOCK ##################
}
    ############################# KEEP THIS BLOCK ##################


############################# KEEP THIS BLOCK ##################
def myanalysis(logger, h, ev, dataset, isData, histAxisName, year, xsec, sow, pass_options, doweight=True):
    from modules.hcoll import hcoll,binning
    hists = hcoll(h, isData, xsec, sow, doweight, process=histAxisName)
    ET.autolog(f"{len(ev)} Events at the start of your analysis", logger, 'i')
############################# KEEP THIS BLOCK ##################

    # Start your analysis``
    #-------------------------------------------------------------------------------------------------------

    if not isData:
         if pass_options=='Xsecweight':
            genw = ev["genWeight"]
            ev["weight_norm"] = (xsec / sow) * genw
            #ev["weight_norm"] =1
         else:
            
            ev["weight_norm"]=1/ev['nAnalysisEvents']


    events["recoTau"]=events.Tau[(events.Tau.idDeepTau2017v2p1VSe >= 16) & (events.Tau.idDeepTau2017v2p1VSjet >= 16) (events.Tau.idDeepTau2017v2p1VSmu >= 4) & (events.Tau.pt > 30) &  (abs(events.Tau.eta)<2.5)]
    events["recoEle"]=events.Electron[(events.Electron.cutBased >=3) & (events.Electron.pt > 25) & (abs(events.Electron.eta)<2.5)]
    events["recoMu"]=events.Muon[(events.Muon.mediumId==True) & (events.Muon.pt > 20) & (abs(events.Muon.eta)<2.1)]
    events["recoPho"]=events.Photon[(events.Photon.cutBased >=2) & (events.Photon.pt > 20) & (abs(events.Photon.eta)<2.5)]
    

    events["recoEle2"] = (ak.num(events.recoEle) >= 2)
    events["recoMu2"] = (ak.num(events.recoMu) >= 2)
    events["recoTau2"] = (ak.num(events.recoTau) >= 2)

    ev_2Ele = events[events.recoEle2]
    ev_2Ele["drEle0g"]=ev_2Ele.recoPho.delta_r(ev_2Ele.recoEle[:,0])
    events["drEle1g"]=events.recoPho.delta_r(events.recoEle2[:,1])

    events["drMu0g"]=events.recoPho.delta_r(events.recoMu2[:,0])
    events["drMu1g"]=events.recoPho.delta_r(events.recoMu2[:,1])

    events["drTau0g"]=events.recoPho.delta_r(events.recoTau2[:,0])
    events["drTau1g"]=events.recoPho.delta_r(events.recoTau2[:,1])

    events["recoPhoEle"] =events.recoPho[events.drEle0g > 0.4 | events.drEle1g > 0.4]
    events["recoPhoMu"] =events.recoPho[events.drMu0g > 0.4 | events.drMu1g > 0.4]
    events["recoPhoTau"] =events.recoPho[events.drTau0g > 0.4 | events.drTau1g > 0.4]


    events["eleeleGammaObj"] = events.recoPho[:,0]+events.recoEle2[:,0] + events.recoEle2[:,1]
    
    events["mumuGammaObj"] = events.recoPho[:,0]+events.recoMu2[:,0] + events.recoMu2[:,1]
    events["tautauGammaObj"] = events.recoPho[:,0]+events.recoTau2[:,0] + events.recoTau2[:,1]



    events["eleeleGammaObjInvMass"] =  events["eleeleGammaObj"].mass
    events["mumuGammaObjInvMass"] =  events["mumuGammaObj"].mass
    events["tautauGammaObjInvMass"] =  events["tautauGammaObj"].mass


    '''
    hists.fill('M_eeg',events.weight_norm, events["recoPhoEle"]==True, events, M_eeg='eleeleGammaObjInvMass')
    hists.fill('M_mmg',events.weight_norm, events["recoPhoMu"]==True, events, M_eeg='mumuGammaObjInvMass')
    hists.fill('M_ttg',events.weight_norm, events["recoPhoTau"]==True, events, M_eeg='tautauGammaObjInvMass')
    '''
    
    hists.fill('M_eeg',events.weight_norm, ak.num(events.recoTau)>=1, events.recoTau[:,0], M_eeg='pt')
    #hists.fill('M_eeg',events.weight_norm, events["recoPhoEle"]==True, events, M_eeg='eleeleGammaObjInvMass')
    #hists.fill('M_mmg',events.weight_norm, events["recoPhoMu"]==True, events, M_eeg='mumuGammaObjInvMass')
    #hists.fill('M_ttg',events.weight_norm, events["recoPhoTau"]==True, events, M_eeg='tautauGammaObjInvMass')
    
#    mass = events["eleeleGammaObj"].mass

    print(f"Mass is {events.recoTau.pt}")

    ############################# KEEP THIS BLOCK ##################
    ET.autolog(f"{len(ev)} Events at the end of your analysis", logger, 'i')
    return hists.get()
    ############################# KEEP THIS BLOCK ##################
