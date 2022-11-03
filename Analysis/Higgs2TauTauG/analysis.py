import awkward as ak, coffea, copy
from coffea import hist, analysis_tools
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
from coffea.analysis_tools import PackedSelection
import numpy.ma as ma
import numpy as np

class hcoll:

    def __init__(self, h, isData, xsec, sow, doweight, **conf):
        self.h = h
        self.conf = conf
        self.isData = isData
        self.xsec = xsec
        self.sow = sow
        self.doweight=doweight

    def fill(self, name, weights, mask, obj, cat={}, flatten=False, **axes):
        fullhist = {}
        #print('----------########---')
        for ini, axis in enumerate(axes.keys()):
            arrr = eval(f"obj.{axes[axis]}[mask]")
            if flatten:
                if ini==0:
                    fullhist[axis],weights = ak.flatten(ak.zip(arrr,weights))
                    weights=weights[ak.flatten(mask)]
                else:
                    fullhist[axis] = ak.flatten(arrr)
            else:
                if ini==0:
                    weights=weights[mask]
                fullhist[axis] = arrr
        if self.doweight:
            self.h[name].fill(weight=weights, **cat, **fullhist, **self.conf)
        else:
            self.h[name].fill(**cat, **fullhist, **self.conf)

    def get(self):
        return self.h


def myanalysis(logger, h, ev, dataset, isData, histAxisName, year, xsec, sow, pass_options, doweight=True):
    
    hists = hcoll(h, isData, xsec, sow, doweight, process=histAxisName)
    ET.autolog(f"{len(ev)} Events at the start of your analysis", logger, 'i')
    # Start your analysis
    #-------------------------------------------------------------------------------------------------------
    # Create any needed branches
    #-------------------------------------------------------------------------------------------------------
    # Define pass options
    #-------------------------------------------------------------------------------------------------------
    # For MC
    if not isData:
        genw = ev["genWeight"]
        ev["weight_norm"] = (xsec / sow) * genw
    #-------------------------------------------------------------------------------------------------------
    # Masks
    #-------------------------------------------------------------------------------------------------------
    #Dilepton events
    #-------------------------------------------------------------------------------------------------------
    #Special masks
    #-------------------------------------------------------------------------------------------------------
    # Fill histograms
    hists.fill('ElectronPt',ev.weight_norm, (abs(ev.lightlepton[:,0].pdgId) ==11), ev.lightlepton[:,0], ElectronPt='pt')

    #-------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------
    #End your analysis
    #-------------------------------------------------------------------------------------------------------
    ET.autolog(f"{len(ev)} Events at the end of your analysis", logger, 'i')
    return hists.get()

def binning(a,b,c):
    return list(np.arange(a,b+c,c))
histograms = {
    'ElectronPt':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('ElectronPt', '$ElectronPt$', binning(0,50,1)))
}
