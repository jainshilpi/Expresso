#!/usr/bin/env python
import awkward as ak
import coffea as coffea
import copy
from coffea import hist,analysis_tools
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
#from modules.hcoll import hcoll
from coffea.analysis_tools import PackedSelection
#####################################################################################################################

class hcoll:
    def __init__(self,h,isData,xsec,sow,**conf):
        self.h=h
        self.conf=conf
        self.isData=isData
        self.xsec=xsec
        self.sow=sow
    def add(self,name,mask,obj,cat={},flatten=False,**axes):
        fullhist={}
        for ini,axis in enumerate(axes.keys()):
            arrr=obj[mask][axes[axis]]
            if flatten:
                fullhist[axis]=ak.flatten(arrr)
            else:
                fullhist[axis]=arrr

            #if ini==0:
            #    weights_obj_base = analysis_tools.Weights(len(fullhist[axis]),storeIndividual=True)
            #    if not self.isData:
            #        weights_obj_base.add("norm",(self.xsec/self.sow)*np.ones_like(fullhist[axis]))
                # if ini==0:
                #     weights_obj_base = analysis_tools.Weights(len(fullhist[axis]),storeIndividual=True)
                #     if not isData:
                #         weights_obj_base.add("norm",(xsec/sow)*np.ones(fullhist[axis]))
        self.h[name].fill(**cat,**fullhist,**self.conf)
    def get(self):
        return self.h
    
def myanalysis(logger,h,ev,dataset,isData,histAxisName,year,xsec,sow,pass_options):
    ET.autolog(f'{len(ev)} Events at the start of your analysis',logger,'i')
    #------------------------Start your analysis below this

    #----------
    ev.one=ak.ones_like(ev.event)
    ev.el=ev.ele_fo
    ev.el["abseta"]=abs(ev.el.eta)
    ev.mu=ev.mu_fo
    ev.jets=ev.goodJets
    ev.el.isTightLep = obj.tightSelElec(ev.el.isFO, ev.el.mvaTTH)
    
    ev.el = ev.el[ev.el.isPres & ev.el.isLooseE & ev.el.isFO & ev.el.isTightLep & (ev.el.tightCharge>=2)]
    #----------
    if pass_options=='2e':
        ev.el=ev.el[(ak.num(ev.el)==2)]
    #----------

    #weights_object_base = analysis_tools.Weights(len(ev),storeIndividual=True)
    if not isData:
        genw= ak.ones_like(ev.event)
        ev.weight_norm=(xsec/sow)*genw
    
    isflip = (ev.el.gen_pdgId == -ev.el.pdgId)
    noflip = (ev.el.gen_pdgId == ev.el.pdgId)
    isprompt = ((ev.el.genPartFlav==1) | (ev.el.genPartFlav == 15))
    truthFlip_mask   = ak.fill_none((isflip & isprompt),False)
    truthNoFlip_mask = ak.fill_none((noflip & isprompt),False)
    e2 = (ak.num(ev.el)==2)
    ev.elof2 = ak.pad_none(ev.el, 2)

    ev.el0 = ev.elof2[:,0]
    isflipel0 = (ev.el0.gen_pdgId == -ev.el0.pdgId)
    noflipel0 = (ev.el0.gen_pdgId == ev.el0.pdgId)
    ispromptel0 = ((ev.el0.genPartFlav==1) | (ev.el0.genPartFlav == 15))
    truthFlip_maskel0   = ak.fill_none((isflipel0 & ispromptel0),False)
    truthNoFlip_maskel0 = ak.fill_none((noflipel0 & ispromptel0),False)

    ev.el1 = ev.elof2[:,1]
    isflipel1 = (ev.el1.gen_pdgId == -ev.el1.pdgId)
    noflipel1 = (ev.el1.gen_pdgId == ev.el1.pdgId)
    ispromptel1 = ((ev.el1.genPartFlav==1) | (ev.el1.genPartFlav == 15))
    truthFlip_maskel1   = ak.fill_none((isflipel1 & ispromptel1),False)
    truthNoFlip_maskel1 = ak.fill_none((noflipel1 & ispromptel1),False)
    
    el0_E =  ET.in_range_mask(abs(ev.el0.eta),lo_lim=1.479,hi_lim=2.5)
    el1_E =  ET.in_range_mask(abs(ev.el1.eta),lo_lim=1.479,hi_lim=2.5)
    el0_B =  ET.in_range_mask(abs(ev.el0.eta),lo_lim=None,hi_lim=1.479)
    el1_B =  ET.in_range_mask(abs(ev.el1.eta),lo_lim=None,hi_lim=1.479)

    el0_H =  ET.in_range_mask(ev.el0.pt,lo_lim=50.0,hi_lim=None)
    el1_H =  ET.in_range_mask(ev.el1.pt,lo_lim=50.0,hi_lim=None)
    el0_M =  ET.in_range_mask(ev.el0.pt,lo_lim=25.0,hi_lim=50.0)
    el1_M =  ET.in_range_mask(ev.el1.pt,lo_lim=25.0,hi_lim=50.0)
    el0_L =  ET.in_range_mask(ev.el0.pt,lo_lim=15.0,hi_lim=25.0)
    el1_L =  ET.in_range_mask(ev.el1.pt,lo_lim=15.0,hi_lim=25.0)


    flipdict = {
        
        "BL_BL" : el0_B & el0_L & el1_B & el1_L,
        "BL_BM" : (el0_B & el0_L & el1_B & el1_M) | (el0_B & el0_M & el1_B & el1_L),
        "BM_BM" : el0_B & el0_M & el1_B & el1_M,
        "BL_BH" : (el0_B & el0_L & el1_B & el1_H) | (el0_B & el0_H & el1_B & el1_L),
        "BM_BH" : (el0_B & el0_M & el1_B & el1_H) | (el0_B & el0_H & el1_B & el1_M),
        "BH_BH" : el0_B & el0_H & el1_B & el1_H,
        "EL_EL" : el0_E & el0_L & el1_E & el1_L,
        "EL_EM" : (el0_E & el0_L & el1_E & el1_M) | (el0_E & el0_H & el1_B & el1_L),
        "EM_EM" : el0_E & el0_M & el1_E & el1_M,
        "EL_EH" : (el0_E & el0_L & el1_E & el1_H) | (el0_E & el0_H & el1_E & el1_L),
        "EM_EH" : (el0_E & el0_M & el1_E & el1_H) | (el0_E & el0_H & el1_E & el1_M),
        "EH_EH" : el0_E & el0_H & el1_E & el1_H,
        "BL_EL" : (el0_B & el0_L & el1_E & el1_L) | (el0_E & el0_L & el1_B & el1_L),
        "EL_BM" : (el0_E & el0_L & el1_B & el1_M) | (el0_B & el0_M & el1_E & el1_L),
        "BL_EM" : (el0_B & el0_L & el1_E & el1_M) | (el0_E & el0_M & el1_B & el1_L),
        "BM_EM" : (el0_B & el0_M & el1_E & el1_M) | (el0_E & el0_M & el1_B & el1_M),
        "EL_BH" : (el0_E & el0_L & el1_B & el1_H) | (el0_B & el0_H & el1_E & el1_L),
        "BL_EH" : (el0_B & el0_L & el1_E & el1_H) | (el0_E & el0_H & el1_B & el1_L),
        "EM_BH" : (el0_E & el0_M & el1_B & el1_H) | (el0_B & el0_H & el1_E & el1_M),
        "BM_EH" : (el0_B & el0_M & el1_E & el1_H) | (el0_E & el0_H & el1_B & el1_M),        
        "BH_EH" : (el0_B & el0_H & el1_E & el1_H) | (el0_E & el0_H & el1_B & el1_H)
        }

    ev["Nele"]=ak.num(ev.el)
    
    hists=hcoll(h,isData,xsec,sow,sam=histAxisName)
    hists.add("Nele", (ev.one==1), ev, Nele="Nele")
    hists.add("pteta", truthFlip_mask|truthNoFlip_mask, ev.el, flatten=True, pt="pt",abseta="abseta")
    hists.add("pteta_flip", truthFlip_mask, ev.el, flatten=True, pt="pt",abseta="abseta")
    hists.add("pteta_noflip", truthNoFlip_mask, ev.el, flatten=True, pt="pt",abseta="abseta")
    hists.add("pteta_el0",(truthFlip_maskel0|truthNoFlip_maskel0),ev.el0,pt="pt",abseta="abseta")
    hists.add("pteta_flip_el0",truthFlip_maskel0,ev.el0,pt="pt",abseta="abseta")
    hists.add("pteta_noflip_el0",truthNoFlip_maskel0,ev.el0,pt="pt",abseta="abseta")
    hists.add("pteta_el1",(truthFlip_maskel1|truthNoFlip_maskel1),ev.el1,pt="pt",abseta="abseta")
    hists.add("pteta_flip_el1",truthFlip_maskel1,ev.el1,pt="pt",abseta="abseta")
    hists.add("pteta_noflip_el1",truthNoFlip_maskel1,ev.el1,pt="pt",abseta="abseta")
    
    for key in flipdict.keys():
        hists.add("pteta_flip_bins",truthFlip_mask & flipdict[key] & e2,ev.elof2,cat={"Flipbins":key},flatten=True,pt="pt",abseta="abseta")
        hists.add("pteta_Noflip_bins",truthNoFlip_mask & flipdict[key] & e2,ev.elof2,cat={"Flipbins":key},flatten=True,pt="pt",abseta="abseta")
    h=hists.get()
        
    # for key in flipdict.keys():
    #       mask = truthFlip_mask & flipdict[key] & e2
    #       hconfig={#"weights_object":weights_object_base[mask],
    #                "sam":histAxisName}
    #       dense_objs_flat = ak.flatten(ev.elof2[mask])
    #       h["pteta_flip_bins"].fill(Flipbins=key,pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),**hconfig)
    #       #                                    weight=weights_object_base.weight(None))

    #       mask=truthNoFlip_mask & flipdict[key] & e2
    #       dense_objs_flat = ak.flatten(ev.elof2[mask])
    #       h["pteta_Noflip_bins"].fill(Flipbins=key,pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),**hconfig)
    #  #                                 weight=weights_object_base.weight(None))
         
    #ev.genw = ak.ones_like(ev.event)
    # for histname in histmasks.keys():
    #     mask,ob = histmasks[histname]
    #     #myev = copy.deepcopy(ev[mask])
    #     print(len(ev))
    #     print(mask)
    #     print(histname)
    #     print(len(ob[mask]))
    #     #genw= ak.ones_like(ob[mask])
    #     #weights_obj_base = analysis_tools.Weights(len(obj[mask]),storeIndividual=True)
    #     #if not isData:
    #     #        weights_obj_base.add("norm",(xsec/sow)*(genw[mask]))

    #     hconfig={#"weight":weights_obj_base.weight(None),
    #              "sam":histAxisName}
        
    #     if 'Nele' in histname:
    #         h[histname].fill(Nele=ak.num(ob[mask]),**hconfig)
    #     elif 'el0' in histname:
    #         dense_objs_flat = ob[mask]
    #         h[histname].fill(pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),**hconfig)
    #     elif 'el1' in histname:
    #         dense_objs_flat = ob[mask]
    #         h[histname].fill(pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),**hconfig)
    #     else:
    #         dense_objs_flat = ak.flatten(ob[mask])
    #         h[histname].fill(pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),**hconfig)


    #------------------------End your analysis here

    ET.autolog(f'{len(ev)} Events at the end of your analysis',logger,'i')
    return h
    #######################  Define your analysis here ##########################################

    
histograms={
    "Nele" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("Nele", "$N_el$", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]),
    ),
    "pteta" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_noflip" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_flip" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_el0" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_noflip_el0" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_flip_el0" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_el1" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_noflip_el1" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_flip_el1" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),

    "pteta_flip_bins" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Cat("Flipbins", "Flipbins","placement"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    ),
    "pteta_Noflip_bins" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Cat("Flipbins", "Flipbins","placement"),
        hist.Bin("pt", "$p_T$", [0,10,25,50,200]),
        hist.Bin("abseta", "|$\eta$|", [0,1.479,2.5]),
    )
}
