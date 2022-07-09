import awkward as ak, coffea, copy
from coffea import hist, analysis_tools
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
from coffea.analysis_tools import PackedSelection
import numpy.ma as ma

class hcoll:

    def __init__(self, h, isData, xsec, sow, doweight=False, **conf):
        self.h = h
        self.conf = conf
        self.isData = isData
        self.xsec = xsec
        self.sow = sow
        self.doweight = doweight

    def fill(self, name, mask, obj, cat={}, flatten=False, **axes):
        fullhist = {}
        for ini, axis in enumerate(axes.keys()):
            arrr = eval(f"obj.{axes[axis]}[mask]")
            if flatten:
                fullhist[axis] = ak.flatten(arrr)
            else:
                fullhist[axis] = arrr
            if ini == 0 and self.doweight:
                weights = self.xsec / self.sow * np.ones_like(fullhist[axis])

        if self.doweight:
            (self.h[name].fill)(weight=weights, **cat, **fullhist, **self.conf)
        else:
            (self.h[name].fill)(**cat, **fullhist, **self.conf)

    def get(self):
        return self.h


def myanalysis(logger, h, ev, dataset, isData, histAxisName, year, xsec, sow, pass_options, doweight=False):
    
    hists = hcoll(h, isData, xsec, sow, doweight=doweight, sam=histAxisName)
    ET.autolog(f"{len(ev)} Events at the start of your analysis", logger, 'i')
    # Start your analysis
    #-------------------------------------------------------------------------------------------------------
    # Create any needed branches
    ev['one'] = ak.ones_like(ev.event)
    ev['el'] = ev.ele_fo
    ev[('el', 'abseta')] = abs(ev.el.eta)
    ev[('el', 'isTightLep')] = obj.tightSelElec(ev.el.isFO, ev.el.mvaTTH)
    ev['el'] = ev.el[(ev.el.isPres & ev.el.isLooseE & ev.el.isFO & ev.el.isTightLep & (ev.el.tightCharge >= 2))]
    ev['Nele'] = ak.num(ev.el)
    ev['mu'] = ev.mu_fo
    ev['jets'] = ev.goodJets
    #-------------------------------------------------------------------------------------------------------
    # Define pass options
    if pass_options == '2e':
        ev = ev[(ak.num(ev.el) == 2)]
    #-------------------------------------------------------------------------------------------------------
    # For MC
    if not isData:
        genw = ak.ones_like(ev.event)
        ev.weight_norm = xsec / sow * genw
    #-------------------------------------------------------------------------------------------------------
    # Masks
    ev[('el', 'isflip')] = ev.el.gen_pdgId == -ev.el.pdgId
    ev[('el', 'noflip')] = ev.el.gen_pdgId == ev.el.pdgId
    ev[('el', 'isprompt')] = (ev.el.genPartFlav == 1) | (ev.el.genPartFlav == 15)
    ev[('el', 'truthFlip')] = ak.fill_none(ev.el.isflip & ev.el.isprompt, False)
    ev[('el', 'truthNoFlip')] = ak.fill_none(ev.el.noflip & ev.el.isprompt, False)
    ev['is2e'] = ak.num(ev.el) == 2
    #-------------------------------------------------------------------------------------------------------
    #Dilepton events
    ev_ee = ev[(ak.num(ev.el) == 2)]
    ev_ee.el0 = ev_ee.el[:, 0]
    ev_ee.el1 = ev_ee.el[:, 1]
    #-------------------------------------------------------------------------------------------------------
    #Special masks
    el0_E = ET.in_range_mask((abs(ev_ee.el0.eta)), lo_lim=1.479, hi_lim=2.5)
    el1_E = ET.in_range_mask((abs(ev_ee.el1.eta)), lo_lim=1.479, hi_lim=2.5)
    el0_B = ET.in_range_mask((abs(ev_ee.el0.eta)), lo_lim=None, hi_lim=1.479)
    el1_B = ET.in_range_mask((abs(ev_ee.el1.eta)), lo_lim=None, hi_lim=1.479)
    el0_H = ET.in_range_mask((ev_ee.el0.pt), lo_lim=50.0, hi_lim=None)
    el1_H = ET.in_range_mask((ev_ee.el1.pt), lo_lim=50.0, hi_lim=None)
    el0_M = ET.in_range_mask((ev_ee.el0.pt), lo_lim=25.0, hi_lim=50.0)
    el1_M = ET.in_range_mask((ev_ee.el1.pt), lo_lim=25.0, hi_lim=50.0)
    el0_L = ET.in_range_mask((ev_ee.el0.pt), lo_lim=15.0, hi_lim=25.0)
    el1_L = ET.in_range_mask((ev_ee.el1.pt), lo_lim=15.0, hi_lim=25.0)

    flipdict = {
        'BL_BL':el0_B & el0_L & el1_B & el1_L, 
        'BL_BM':el0_B & el0_L & el1_B & el1_M | el0_B & el0_M & el1_B & el1_L, 
        'BM_BM':el0_B & el0_M & el1_B & el1_M, 
        'BL_BH':el0_B & el0_L & el1_B & el1_H | el0_B & el0_H & el1_B & el1_L, 
        'BM_BH':el0_B & el0_M & el1_B & el1_H | el0_B & el0_H & el1_B & el1_M, 
        'BH_BH':el0_B & el0_H & el1_B & el1_H, 
        'EL_EL':el0_E & el0_L & el1_E & el1_L, 
        'EL_EM':el0_E & el0_L & el1_E & el1_M | el0_E & el0_H & el1_B & el1_L, 
        'EM_EM':el0_E & el0_M & el1_E & el1_M, 
        'EL_EH':el0_E & el0_L & el1_E & el1_H | el0_E & el0_H & el1_E & el1_L, 
        'EM_EH':el0_E & el0_M & el1_E & el1_H | el0_E & el0_H & el1_E & el1_M, 
        'EH_EH':el0_E & el0_H & el1_E & el1_H, 
        'BL_EL':el0_B & el0_L & el1_E & el1_L | el0_E & el0_L & el1_B & el1_L, 
        'EL_BM':el0_E & el0_L & el1_B & el1_M | el0_B & el0_M & el1_E & el1_L, 
        'BL_EM':el0_B & el0_L & el1_E & el1_M | el0_E & el0_M & el1_B & el1_L, 
        'BM_EM':el0_B & el0_M & el1_E & el1_M | el0_E & el0_M & el1_B & el1_M, 
        'EL_BH':el0_E & el0_L & el1_B & el1_H | el0_B & el0_H & el1_E & el1_L, 
        'BL_EH':el0_B & el0_L & el1_E & el1_H | el0_E & el0_H & el1_B & el1_L, 
        'EM_BH':el0_E & el0_M & el1_B & el1_H | el0_B & el0_H & el1_E & el1_M, 
        'BM_EH':el0_B & el0_M & el1_E & el1_H | el0_E & el0_H & el1_B & el1_M, 
        'BH_EH':el0_B & el0_H & el1_E & el1_H | el0_E & el0_H & el1_B & el1_H
    }
    #-------------------------------------------------------------------------------------------------------
    # Fill histograms
    hists.fill('Nele', (ev.one == 1), ev, Nele='Nele')
    hists.fill('allel', (ev.el.truthFlip | ev.el.truthNoFlip), (ev.el), flatten=True, pt='pt', abseta='abseta')
    hists.fill('allel_flip', (ev.el.truthFlip), (ev.el), flatten=True, pt='pt', abseta='abseta')
    hists.fill('el0', (ev_ee.el0.truthFlip | ev_ee.el0.truthNoFlip), (ev_ee.el0), pt='pt', abseta='abseta')
    hists.fill('el0_flip', (ev_ee.el0.truthFlip), (ev_ee.el0), pt='pt', abseta='abseta')
    hists.fill('el1', (ev_ee.el1.truthFlip | ev_ee.el1.truthNoFlip), (ev_ee.el1), pt='pt', abseta='abseta')
    hists.fill('el1_flip', (ev_ee.el1.truthFlip), (ev_ee.el1), pt='pt', abseta='abseta')

    for key in flipdict.keys():
        hists.fill('pteta_flip_bins', (ev_ee.el.truthFlip & flipdict[key]), (ev_ee.el), cat={'Flipbins': key}, flatten=True, pt='pt', abseta='abseta')
        hists.fill('pteta_Noflip_bins', (ev_ee.el.truthNoFlip & flipdict[key]), (ev_ee.el), cat={'Flipbins': key}, flatten=True, pt='pt', abseta='abseta')
    #-------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------
    #End your analysis
    #-------------------------------------------------------------------------------------------------------
    ET.autolog(f"{len(ev)} Events at the end of your analysis", logger, 'i')
    return hists.get()


histograms = {
    'Nele':hist.Hist('Events',
                     hist.Cat('sam', 'sam'),
                     hist.Bin('Nele', '$N_el$', [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])),
    
    'allel':hist.Hist('Events',
                      hist.Cat('sam', 'sam'),
                      hist.Bin('pt', '$p_T$', [0, 10, 25, 50, 200]),
                      hist.Bin('abseta', '|$\\eta$|', [0, 1.479, 2.5])),
    
    'el0':hist.Hist('Events',
                    hist.Cat('sam', 'sam'),
                    hist.Bin('pt', '$p_T$', [0, 10, 25, 50, 200]),
                    hist.Bin('abseta', '|$\\eta$|', [0, 1.479, 2.5])),
    
    'el1':hist.Hist('Events',
                    hist.Cat('sam', 'sam'),
                    hist.Bin('pt', '$p_T$', [0, 10, 25, 50, 200]),
                    hist.Bin('abseta', '|$\\eta$|', [0, 1.479, 2.5])),
    
    'allel_flip':hist.Hist('Events',
                           hist.Cat('sam', 'sam'),
                           hist.Bin('pt', '$p_T$', [0, 10, 25, 50, 200]),
                           hist.Bin('abseta', '|$\\eta$|', [0, 1.479, 2.5])),
    
    'el0_flip':hist.Hist('Events',
                         hist.Cat('sam', 'sam'),
                         hist.Bin('pt', '$p_T$', [0, 10, 25, 50, 200]),
                         hist.Bin('abseta', '|$\\eta$|', [0, 1.479, 2.5])),
    
    'el1_flip':hist.Hist('Events',
                         hist.Cat('sam', 'sam'),
                         hist.Bin('pt', '$p_T$', [0, 10, 25, 50, 200]),
                         hist.Bin('abseta', '|$\\eta$|', [0, 1.479, 2.5])),
    
    'pteta_flip_bins':hist.Hist('Events',
                                hist.Cat('sam', 'sam'),
                                hist.Cat('Flipbins', 'Flipbins', 'placement'),
                                hist.Bin('pt', '$p_T$', [0, 10, 25, 50, 200]),
                                hist.Bin('abseta', '|$\\eta$|', [0, 1.479, 2.5])),
    
    
    'pteta_Noflip_bins':hist.Hist('Events',
                                  hist.Cat('sam', 'sam'),
                                  hist.Cat('Flipbins', 'Flipbins', 'placement'),
                                  hist.Bin('pt', '$p_T$', [0, 10, 25, 50, 200]),
                                  hist.Bin('abseta', '|$\\eta$|', [0, 1.479, 2.5]))
}
