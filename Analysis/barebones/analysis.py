import awkward as ak, coffea, copy
from coffea import hist, analysis_tools
from modules.selection import *
import modules.ExpressoTools as ET
import modules.objects as obj
from coffea.analysis_tools import PackedSelection
import numpy.ma as ma
from modules.hcoll import binning

histograms = {
    'Nele':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Nele', '$N_{el}$', [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])),
    'Nmu':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Nmu', '$N_{mu}$', [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])),

    'Nele_withcut':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Nele', '$N_{el}$', [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])),
    'Nmu_withcut':hist.Hist('Events',hist.Cat('process', 'process'),hist.Bin('Nmu', '$N_{mu}$', [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])),
    
}


def myanalysis(pars,logger, h, ev, doweight=True):

    dataset,isData,histAxisName,year=pars['dataset'],pars['isData'],pars['histAxisName'],pars['year']
    xsec,sow,pass_options=pars['xsec'],pars['sow'],pars['passoptions']
    from modules.hcoll import hcoll,binning
    hists = hcoll(h, isData, xsec, sow, doweight, process=histAxisName)
    ET.autolog(f"{len(ev)} Events at the start of your analysis", logger, 'i')

    # Start your analysis
    #-------------------------------------------------------------------------------------------------------
    # Create any needed branches
    ev['one'] = ak.ones_like(ev.event)
    #-------------------------------------------------------------------------------------------------------
    # Define pass options
    if pass_options == '3e': ## this pass_options can be passed via expresso.py using --PassOptions something-something
        ev = ev[(ak.num(ev.ele) == 3)]
    #-------------------------------------------------------------------------------------------------------
    # For MC
    if not isData: ## this is read from the json automatically
        genw = ev["genWeight"]
        ev["weight_norm"] = (xsec / sow) * genw

    eventcoll=ev
    norm=eventcoll.weight_norm
    basic_sel=(eventcoll.one == 1)
    
    hists.fill('Nele',norm, basic_sel, eventcoll, Nele='Nele')
    hists.fill('Nmu',norm, basic_sel, eventcoll, Nmu='Nmu')

    eventcoll=ev
    norm=eventcoll.weight_norm
    basic_sel=(eventcoll.Nele == 1)
    
    hists.fill('Nele_withcut',norm, basic_sel, eventcoll, Nele='Nele')
    hists.fill('Nmu_withcut',norm, basic_sel, eventcoll, Nmu='Nmu')
    
    #-------------------------------------------------------------------------------------------------------
    
    #End your analysis
    #-------------------------------------------------------------------------------------------------------
    ET.autolog(f"{len(ev)} Events at the end of your analysis", logger, 'i')
    return hists.get()


