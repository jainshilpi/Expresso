from coffea.analysis_tools import PackedSelection
import awkward as ak
from modules.ecuts import cutflow

def preselection(isData,events,out):

    #-----------Add your pre selection here----------------------#
    #-------------------------------------------------------------
    selections = PackedSelection(dtype='uint64')
    selections.add("leadingelectronpt>5",ak.pad_none(events.Electron,1).pt[:,0] > 0)
    #selections.add("sub-leadingelectronpt>10",ak.pad_none(events.Electron,2).pt[:,1] > 10)
    #-------------------------------------------------------------
    out=cutflow(out,events,selections,cumulative=True,printit=False)
    return events[selections.all(*selections.names)],out
    #-------------------------------------------------------------
    
    



