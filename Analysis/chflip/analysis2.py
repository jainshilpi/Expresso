#!/usr/bin/env python
import awkward as ak
import coffea as coffea
from coffea import hist
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
from coffea.analysis_tools import PackedSelection
#####################################################################################################################


def myanalysis(logger,h,ev,dataset,isData,histAxisName,year,xsec,sow):
    ET.autolog(f'{len(ev)} Events at the start of your analysis',logger,'i')

    #------------------------Start your analysis below this

    #----------
    el=ev.ele_fo
    mu=ev.mu_fo
    jets=ev.goodJets
    #----------

    def in_range_mask(in_var,lo_lim=None,hi_lim=None):
        if (lo_lim is None) and (hi_lim is None):
            raise Exception("Error: No cuts specified")
        if lo_lim is not None:
            above_min = (in_var > lo_lim)
        else:
            above_min = (ak.ones_like(in_var)==1)
        if hi_lim is not None:
            below_max = (in_var <= hi_lim)
        else:
            below_max = (ak.ones_like(in_var)==1)
        return ak.fill_none((above_min & below_max),False)

    el["isTightLep"] = obj.tightSelElec(el.isFO, el.mvaTTH)
    el = el[el.isPres & el.isLooseE & el.isFO & el.isTightLep & (el.tightCharge>=2)]

    nomask= (1>0)
    isflip = (el.gen_pdgId == -el.pdgId)
    noflip = (el.gen_pdgId == el.pdgId)
    isprompt = ((el.genPartFlav==1) | (el.genPartFlav == 15))
    truthFlip_mask   = ak.fill_none((isflip & isprompt),False)
    truthNoFlip_mask = ak.fill_none((noflip & isprompt),False)
    e2 = (ak.num(el)==2)
    elof2 = ak.pad_none(el, 2)
    el0 = elof2[:,0]
    el1 = elof2[:,1]
    el0_E =  in_range_mask(abs(el0.eta),lo_lim=1.479,hi_lim=2.5)
    el1_E =  in_range_mask(abs(el1.eta),lo_lim=1.479,hi_lim=2.5)
    el0_B =  in_range_mask(abs(el0.eta),lo_lim=None,hi_lim=1.479)
    el1_B =  in_range_mask(abs(el1.eta),lo_lim=None,hi_lim=1.479)

    el0_H =  in_range_mask(el0.pt,lo_lim=50.0,hi_lim=None)
    el1_H =  in_range_mask(el1.pt,lo_lim=50.0,hi_lim=None)
    el0_M =  in_range_mask(el0.pt,lo_lim=25.0,hi_lim=50.0)
    el1_M =  in_range_mask(el1.pt,lo_lim=25.0,hi_lim=50.0)
    el0_L =  in_range_mask(el0.pt,lo_lim=15.0,hi_lim=25.0)
    el1_L =  in_range_mask(el1.pt,lo_lim=15.0,hi_lim=25.0)


    flipdict = {
            "EH_EH" : el0_E & el0_H & el1_E & el1_H,
            "BH_EH" : el0_B & el0_H & el1_E & el1_H,
            "EM_EH" : el0_E & el0_M & el1_E & el1_H,
            "BM_EH" : el0_B & el0_M & el1_E & el1_H,
            "EL_EH" : el0_E & el0_L & el1_E & el1_H,
            "BL_EH" : el0_B & el0_L & el1_E & el1_H,

            "EH_BH" : el0_E & el0_H & el1_B & el1_H,
            "BH_BH" : el0_B & el0_H & el1_B & el1_H,
            "EM_BH" : el0_E & el0_M & el1_B & el1_H,
            "BM_BH" : el0_B & el0_M & el1_B & el1_H,
            "EL_BH" : el0_E & el0_L & el1_B & el1_H,
            "BL_BH" : el0_B & el0_L & el1_B & el1_H,

            "EH_EM" : el0_E & el0_H & el1_E & el1_M,
            "BH_EM" : el0_B & el0_H & el1_E & el1_M,
            "EM_EM" : el0_E & el0_M & el1_E & el1_M,
            "BM_EM" : el0_B & el0_M & el1_E & el1_M,
            "EL_EM" : el0_E & el0_L & el1_E & el1_M,
            "BL_EM" : el0_B & el0_L & el1_E & el1_M,

            "EH_BM" : el0_E & el0_H & el1_B & el1_M,
            "BH_BM" : el0_B & el0_H & el1_B & el1_M,
            "EM_BM" : el0_E & el0_M & el1_B & el1_M,
            "BM_BM" : el0_B & el0_M & el1_B & el1_M,
            "EL_BM" : el0_E & el0_L & el1_B & el1_M,
            "BL_BM" : el0_B & el0_L & el1_B & el1_M,

            "EH_EL" : el0_E & el0_H & el1_E & el1_L,
            "BH_EL" : el0_B & el0_H & el1_E & el1_L,
            "EM_EL" : el0_E & el0_M & el1_E & el1_L,
            "BM_EL" : el0_B & el0_M & el1_E & el1_L,
            "EL_EL" : el0_E & el0_L & el1_E & el1_L,
            "BL_EL" : el0_B & el0_L & el1_E & el1_L,

            "EH_BL" : el0_E & el0_H & el1_B & el1_L,
            "BH_BL" : el0_B & el0_H & el1_B & el1_L,
            "EM_BL" : el0_E & el0_M & el1_B & el1_L,
            "BM_BL" : el0_B & el0_M & el1_B & el1_L,
            "EL_BL" : el0_E & el0_L & el1_B & el1_L,
            "BL_BL" : el0_B & el0_L & el1_B & el1_L,
        }



    histmasks={
        "Nele":nomask,
        "ptabseta":(truthFlip_mask|truthNoFlip_mask),
        "ptabseta_flip":truthFlip_mask,
        "ptabseta_noflip":truthNoFlip_mask,
        "ptabseta_el0":(truthFlip_mask|truthNoFlip_mask) & e2,
        "ptabseta_flip_el0":truthFlip_mask & e2,
        "ptabseta_noflip_el0":truthNoFlip_mask & e2,
        "ptabseta_el1":(truthFlip_mask|truthNoFlip_mask) & e2,
        "ptabseta_flip_el1":truthFlip_mask & e2,
        "ptabseta_noflip_el1":truthNoFlip_mask & e2}

    for key in flipdict.keys():
        dense_objs_flat = ak.flatten(elof2[truthFlip_mask & flipdict[key] & e2])
        h["ptabseta_flip_bins"].fill(Flipbins=key,pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),sam=histAxisName)

        dense_objs_flat = ak.flatten(elof2[truthNoFlip_mask & flipdict[key] & e2])
        h["ptabseta_Noflip_bins"].fill(Flipbins=key,pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),sam=histAxisName)

    for histname in histmasks.keys():
        print(histname)
        if 'Nele' in histname:
            h[histname].fill(Nele=ak.num(el),sam=histAxisName)
        elif 'el0' in histname:
            dense_objs_flat = ak.flatten(el0[histmasks[histname]])
            h[histname].fill(pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),sam=histAxisName)
        elif 'el1' in histname:
            dense_objs_flat = ak.flatten(el1[histmasks[histname]])
            h[histname].fill(pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),sam=histAxisName)
        else:
            dense_objs_flat = ak.flatten(el[histmasks[histname]])
            h[histname].fill(pt=dense_objs_flat.pt,abseta=abs(dense_objs_flat.eta),sam=histAxisName)


    #------------------------End your analysis here

    ET.autolog(f'{len(ev)} Events at the end of your analysis',logger,'i')
    return h
    #######################  Define your analysis here ##########################################


histograms={
    "Nele" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("Nele", "Nele", [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]),
    ),
    "ptabseta" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_noflip" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_flip" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_el0" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_noflip_el0" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_flip_el0" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_el1" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_noflip_el1" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_flip_el1" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),

    "ptabseta_flip_bins" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Cat("Flipbins", "Flipbins"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    ),
    "ptabseta_Noflip_bins" : hist.Hist(
        "Events",
        hist.Cat("sam", "sam"),
        hist.Cat("Flipbins", "Flipbins"),
        hist.Bin("pt", "pt", [0, 30.0, 45.0, 60.0, 100.0, 200.0]),
        hist.Bin("abseta", "abseta", [0, 0.4, 0.8, 1.1, 1.4, 1.6, 1.9, 2.2, 2.5]),
    )
}
