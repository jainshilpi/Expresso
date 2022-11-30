import numpy as np
import gzip
from pathlib import Path
import yaml
import os
try:
    import pickle5 as pickle
except ImportError:
    import pickle
#import hist
import coffea.hist as hist
from tabulate import tabulate
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 200
import mplhep as hep
from hist.intervals import ratio_uncertainty, clopper_pearson_interval, poisson_interval
import numpy as np

class ExpressoPlotter():
    def __init__(self,year):
        import numpy as np
        import gzip
        import yaml
        import os
        try:
            import pickle5 as pickle
        except ImportError:
            import pickle
        #import hist
        import coffea.hist as hist
        from tabulate import tabulate
        import matplotlib.pyplot as plt
        plt.rcParams['figure.dpi'] = 200
        plt.rcParams['savefig.dpi'] = 200
        import mplhep as hep
        from hist.intervals import ratio_uncertainty, clopper_pearson_interval, poisson_interval
        import numpy as np
        self._files=[]
        self._year=year
        self._plots=[]
        self.plot_live=False
        self.SSaveLocation=''
        
    def settings(self,file):
        path = Path(file)
        with open(path) as stream:
            self._ps = yaml.safe_load(stream)
        
    def get_hist_from_pkl(self, path_to_pkl,allow_empty=True,tohist=False):
        h = pickle.load( gzip.open(path_to_pkl) )
        if not allow_empty:
            h = {k:v for k,v in h.items() if v.values() != {}}
        if tohist:
            return h.to_hist()
        else:
            return h
    def geths(self,h,scale=-1):
        if scale==-1:
            return h*(1/sum(list(h.counts())))
        else:
            return h*scale
    
    def dictprint(self, di):
        for key, value in di.items():
            print(key, ' : ', value)
    
    def geterrratio(self,hi,typeunc='p'):
        ratio = (hi[0].values()/hi[1].values())
        if typeunc=='p':
            err_down, err_up  = ratio_uncertainty(hi[0].values(), hi[1].values(), 'efficiency')
        else:
            err_down, err_up = clopper_pearson_interval(hi[0].values(), hi[1].values())
        labels=[]
        for ra, u, d in zip(ratio.ravel(), err_up.ravel(), err_down.ravel()):
            ra, u, d = f'{ra:.6f}', f'{u:.6f}', f'{d:.6f}'
            st = '$'+ra+'_{-'+d+'}^{+'+u+'}$'
            labels.append(st)
        return ratio,labels
    
    def histolocation(self,loc):
        self._loc=loc
    def savelocation(self,loc):
        self._SSaveLocation=loc
    
    def addfile(self,label,file,color,stack,scale):
        self._files.append({'label':label,'file':file,'color':color,'stack':stack,
                            'scale':scale,
                            'coffehists':self.get_hist_from_pkl(self._loc+'/'+file),
                            'h':self.get_hist_from_pkl(self._loc+'/'+file,True)
                           })

class normalplot():
    def __init__(self,plotter,filename,hi,axis):
        self.plotter=plotter
        self._files=plotter._files
        SSaveLocation=plotter._SSaveLocation
        if plotter._ps['hepstyle']=='ROOT':
            hep.style.use(hep.style.ROOT)
        
        if plotter._ps['hepstyle']=='CMS':
            hep.style.use("CMS")
            hep.cms.label(plotter._ps["PrivateLabel"], data=plotter._ps["withdata"], year=plotter._year)
            
        nostack=[]
        stack=[]
        nostacklabels=[]
        nostackcolors=[]
        stacklabels=[]
        stackcolors=[]
        stackscales=[]
        nostackscales=[]
        
        for file in self._files:
            _h=file['h'][hi]
            print(file['h'][hi])
            _ch=file['coffehists'][hi]
            _color=file['color']
            _stack=file['stack']
            _scale=file['scale']
            _label=file['label']
            project=_ch.project(axis)
            if(_stack=='stack'):
                stack.append(project)
                stacklabels.append(_label)
                stackcolors.append(_color)
                stackscales.append(_scale)
            if(_stack=='nostack'):
                nostack.append(project)
                nostacklabels.append(_label)
                nostackcolors.append(_color)
                nostackscales.append(_scale)
        if len(stack)!=0:
            hep.histplot([plotter.geths(st.to_hist(),scaleit) for st,scaleit in zip(stack,stackscales)],lw=1,stack=True,histtype='fill',label=stacklabels, color=stackcolors)
        if len(nostack)!=0:
            hep.histplot([plotter.geths(nst.to_hist(),scaleit) for nst,scaleit in zip(nostack,nostackscales)],lw=1,stack=False,histtype='step',label=nostacklabels,
                         color=nostackcolors)

        #if 'normal' in allkey or '2D' in allkey:
        plt.tight_layout()
        plt.legend(loc='best',fontsize='x-small',ncol=2,fancybox=True)#,bbox_to_anchor=(0.5, 1.05),ncol=3, fancybox=True, shadow=True)
        plt.savefig(f'{SSaveLocation}/normal_{filename}.pdf', dpi=200)
        plt.close()
