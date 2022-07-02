from modules.corrections import SFevaluator, GetBTagSF, ApplyJetCorrections, GetBtagEff, AttachMuonSF, AttachElectronSF, AttachPerLeptonFR, GetPUSF, ApplyRochesterCorrections, ApplyJetSystematics, AttachPSWeights, AttachPdfWeights, AttachScaleWeights, GetTriggerSF
import modules.ExpressoTools as ET
from modules.selection import *
from modules.objects import *
from coffea.analysis_tools import PackedSelection
from coffea import hist

def cutflow(out,events,selections,printit=False):
    #if cumulative: print(f'cumulative')

    for k,iii in enumerate(range(2)):
        mysel=selections
        sels=[]
        cutflowp=[]
        ne=[]
        cutflowp.append(len(events))
        ne.append(np.ones(len(events)))
        names=["all_events"]
    
        for ss,n in enumerate(mysel.names):
        
            if k==0: ## Cumulative 
                sels.append(n)
        
            else: 
                sels=[n]
    
            
            cutflowp.append(np.count_nonzero(mysel.all(*sels)))
            ne.append(np.ones(np.count_nonzero(mysel.all(*sels)))*(ss+2))        
        
        if printit: print('Cutflow')
        for namesi,ci,ei in zip(names+mysel.names,cutflowp,ne):
            
            if k==0: out['cutflow'].fill(selection=namesi,x=ei)
            else: out['cutflow_individual'].fill(selection=namesi,x=ei)
        if printit: print(out['cutflow'].project("selection").to_hist())
        if printit: print(out['cutflow_individual'].project("selection").to_hist())
    return out


if __name__=="__main__":
    import awkward as ak
    from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
    import numpy as np
    fname = "https://raw.githubusercontent.com/CoffeaTeam/coffea/master/tests/samples/nano_dy.root"
    events = NanoEventsFactory.from_root(fname, schemaclass=NanoAODSchema).events()
    selections = PackedSelection(dtype='uint64')

    selections.add("leadingelectronpt>10",ak.pad_none(events.Electron,1).pt[:,0] > 10)
    selections.add("leadingelectronpt>18",ak.pad_none(events.Electron,1).pt[:,0] > 18)
    selections.add("leadingjetpt>20",events.Jet[:,0].pt > 20)
    selections.add("leadingelectronpt>3",ak.pad_none(events.Electron,1).pt[:,0] > 3)
    selections.add("leadingjetpt>30",events.Jet[:,0].pt > 30)
    selections.add("leadingjetpt>40",events.Jet[:,0].pt > 40)
    
    hii={}
    hii['cutflow']=hist.Hist(axes=[hist.Cat("selection", "selection","placement"),
                                   hist.Bin("x", "x coordinate [m]", 7, 0, 7)],
                             label="Cutflow")
    
    hi=cutflow(hii,events,selections,cumulative=True)
    hip=hi['cutflow'].project('selection')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4))
    print(hip.to_hist())
    hip.to_hist().plot(ax=ax)
    plt.xticks(rotation=90)
    plt.savefig("cutflow.png")
