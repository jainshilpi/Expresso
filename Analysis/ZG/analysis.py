import awkward as ak, coffea, copy
from coffea import hist, analysis_tools
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
from coffea.analysis_tools import PackedSelection
import numpy.ma as ma
import numpy as np
from modules.hcoll import binning
    ############################# KEEP THIS BLOCK ##################
histograms = {
    ############################# KEEP THIS BLOCK ##################
    
    'M_tt':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('M_tt', 'M_tt(GeV)', binning(20,120,1))),
    'M_ee':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('M_ee', 'M_ee(GeV)', binning(20,120,1))),
    'M_uu':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('M_uu', 'M_uu(GeV)', binning(20,120,1))),
    'Tau_pt':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Tau_pt', 'Tau_pt(GeV)', binning(0,300,1))),

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
            ev["weight_norm"]=1

            
    ev_2taus=ev[ak.num(ev.GenTaus)==2]
    ev_2taus["gen_ditau_mass"]=(ev_2taus.GenTaus[:,0]+ev_2taus.GenTaus[:,1]).mass
    hists.fill('M_tt',ev_2taus.weight_norm, ak.num(ev_2taus.GenTaus)==2,ev_2taus , M_tt='gen_ditau_mass')
    hists.fill('Tau_pt',ev_2taus.weight_norm, ak.num(ev_2taus.GenTaus)==2,ev_2taus.GenTaus[:,0] , Tau_pt='pt')
    hists.fill('Tau_pt',ev_2taus.weight_norm, ak.num(ev_2taus.GenTaus)==2,ev_2taus.GenTaus[:,1] , Tau_pt='pt')

    
    ev_2eles=ev[ak.num(ev.GenEles)==2]
    ev_2eles["gen_diele_mass"]=(ev_2eles.GenEles[:,0]+ev_2eles.GenEles[:,1]).mass
    hists.fill('M_ee',ev_2eles.weight_norm, ak.num(ev_2eles.GenEles)>1,ev_2eles , M_ee='gen_diele_mass')    
    
    ev_2mus=ev[ak.num(ev.GenMuons)==2]
    ev_2mus["gen_dimu_mass"]=(ev_2mus.GenMuons[:,0]+ev_2mus.GenMuons[:,1]).mass
    hists.fill('M_uu',ev_2mus.weight_norm, ak.num(ev_2mus.GenMuons)>1,ev_2mus , M_uu='gen_dimu_mass')

    ############################# KEEP THIS BLOCK ##################
    ET.autolog(f"{len(ev)} Events at the end of your analysis", logger, 'i')
    return hists.get()
    ############################# KEEP THIS BLOCK ##################
