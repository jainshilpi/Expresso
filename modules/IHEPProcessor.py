from coffea import processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import hist
import threading
import modules.ExpressoTools as ET

class IHEPProcessor(processor.ProcessorABC):
    def __init__(self,logger,analysisname,varstosave,preprocess,preselect,analysis,histos,samples):
        histos['cutflow']=hist.Hist(axes=[hist.Cat("selection", "selection"),
                                          hist.Bin("x", "x coordinate [m]", 80, 0, 80)],
                                    label="Cutflow")
        self._accumulator = processor.dict_accumulator(histos)
        self._samples = samples
        self._analysis = analysis
        self._preprocess = preprocess
        self._preselect = preselect
        self._varstosave = varstosave
        self._analysisname = analysisname
        self._logger=logger
    @property
    def accumulator(self):
        return self._accumulator

    # we will receive a NanoEvents instead of a coffea DataFrame
    def process(self, events):
        ET.autolog(f'Inside process',self._logger,'i')
        #------- Initialize accumulator with histograms
        try:
            out = self.accumulator.identity()
        except:
            ET.autolog(f'Can not create accumulator of histograms',self._logger,'e')
        #------- preprocess (mostly create objects and special event variables)
        try: events,dataset,isData,histAxisName,year,xsec,sow=self._preprocess(self._samples,events)
        except:             ET.autolog(f'Can not preprocess',self._logger,'e')
        #------- preselect and store cutflow
        events,out=self._preselect(isData,events,out)
        #------- run analysis
        filename=self._varstosave(self._logger,events,histAxisName,'Analysis/'+self._analysisname+'/output/trees/')
        out = self._analysis(self._logger,out,events,dataset,isData,histAxisName,year,xsec,sow)
        #------- return accumulator
        return out

    def postprocess(self, accumulator):
        return accumulator
