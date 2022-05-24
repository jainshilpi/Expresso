from coffea import processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import hist

class IHEPProcessor(processor.ProcessorABC):
    def __init__(self,preprocess,preselect,analysis,histos,samples):
        histos['cutflow']=hist.Hist(axes=[hist.Cat("selection", "selection"),
                                          hist.Bin("x", "x coordinate [m]", 80, 0, 80)],
                                    label="Cutflow")
        self._accumulator = processor.dict_accumulator(histos)
        self._samples = samples
        self._analysis = analysis
        self._preprocess = preprocess
        self._preselect = preselect

    @property
    def accumulator(self):
        return self._accumulator

    # we will receive a NanoEvents instead of a coffea DataFrame
    def process(self, events):
        
        #------- Initialize accumulator with histograms
        out = self.accumulator.identity()
        #------- preprocess (mostly create objects and special event variables)
        events,dataset,isData,histAxisName,year,xsec,sow=self._preprocess(self._samples,events)
        #------- preselect and store cutflow
        events,out=self._preselect(isData,events,out)
        #------- run analysis
        out = self._analysis(out,events,dataset,isData,histAxisName,year,xsec,sow)
        #------- return accumulator
        return out

    def postprocess(self, accumulator):
        return accumulator
