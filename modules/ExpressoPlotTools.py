import gzip
import yaml
from pathlib import Path
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
from hist.intervals import ratio_uncertainty
import numpy as np
def get_hist_from_pkl(path_to_pkl,allow_empty=True):
        h = pickle.load( gzip.open(path_to_pkl) )
        if not allow_empty:
            h = {k:v for k,v in h.items() if v.values() != {}}
        return h


def dictprint(di):
        for key, value in di.items():
                print(key, ' : ', value)

def alldictplot(histodictall,outputfolder,SSaveLocation='./',plotsetting='modules/plotsettings.yaml'):
        path = Path(plotsetting)
        with open(path) as stream:
                ps = yaml.safe_load(stream)
                
        files=histodictall['files'];del histodictall['files']
        year=histodictall['year'];del histodictall['year']
        if SSaveLocation=='./': SSaveLocation='plots'
        os.system(f'mkdir -p {SSaveLocation}')

        for allkey in histodictall.keys():
                print(f'------------{allkey}----------------')
                histodict=histodictall[allkey]
                
                #if ps['hepstyle']=='ROOT':
            
                #if ps['hepstyle']=='CMS':
                #fig, ax = plt.subplots()
                hep.style.use("CMS")
                hep.cms.label(ps["PrivateLabel"], data=ps["withdata"], year=year)
                
                #else:
                #        hep.style.use(hep.style.ROOT)
                #print(f'--{histodict.keys()}--')
                for hiname in histodict.keys():
                        histo=histodict[hiname]
        
                        
        
                        if 'args' in histo.keys():
                                args=histo['args']
                                del histo['args']
            
                        if 'normal' in allkey:
                                nostack=[]
                                stack=[]
                                nostacklabels=[]
                                stacklabels=[]
            
                        for k in histo.keys():
                                #if k == 'args': continue
                                #print(k)
                                scale=1.0
                                if 'scale' in histo[k].keys():
                                        scale=histo[k]['scale']
                                thist=get_hist_from_pkl(outputfolder+"/"+files[histo[k]['file']])[k].to_hist()
                                if '2Dratio' in allkey:
                                        histo[k]['h']=thist.project(histo[k]['xaxis'],histo[k]['yaxis'])
                                else:
                                        histo[k]['h']=thist.project(histo[k]['axis'])
                                        
        
        
                        if 'normal' in allkey:
                                for k in histo.keys():
                                        #if k == 'args': continue
                                        if(histo[k]['stack']==True):
                                                stack.append(histo[k]['h'])
                                                stacklabels.append(args['label'])
                                        if(histo[k]['stack']==False):
                                                nostack.append(histo[k]['h'])
                                                nostacklabels.append(args['label'])
                                if len(stack)!=0:
                                        hep.histplot(stack,lw=3,stack=True,histtype='fill',label=stacklabels,color=args['color'])
                                if len(nostack)!=0:
                                        hep.histplot(nostack,lw=3,stack=False,histtype='step',label=nostacklabels, yerr=True,color=args['color'])
                                #ax.tick_params(axis="x")
                                #plt.xticks(fontsize=7)
                    
                        if 'ratio' in allkey:
                                hi=[]
                                #print(histo.keys())
                                for i,k in enumerate(histo.keys()):
                                        #if k == 'args': continue
                                        hi.append(histo[k]['h'])
                                ratio = (hi[0]/hi[1])
                                err_up, err_down = ratio_uncertainty(hi[0].values(), hi[1].values(), 'poisson-ratio')
                                labels = []
                                for ra, u, d in zip(ratio.values().ravel(), err_up.ravel(), err_down.ravel()):
                                        ra, u, d = f'{ra:.6f}', f'{u:.6f}', f'{d:.6f}'
                                        st = '$'+ra+'_{-'+d+'}^{+'+u+'}$'
                                        labels.append(st)
                                if '2D' in allkey:
                                        fig, ax = plt.subplots(figsize=tuple([z * 10 for z in ratio.values().shape]))
                                        labels = np.array(labels).reshape(ratio.values().shape)
                                        with open(f'{SSaveLocation}/{allkey}.txt', 'w') as fi:
                                                fi.write(f'{labels}')
                                else:
                                        labels = np.array(labels)
                                        data=[]
                                        with open(f'{SSaveLocation}/{allkey}.txt', 'w') as fi:
                                                for i in range(len((hi[0]/hi[1]).view())):
                                                        data.append([(hi[0]/hi[1]).axes[0][i],labels[i]])
                                                fi.write(tabulate(data, headers=["Bin", "Value"]))
                                if '2D' in allkey:
                                        hep.hist2dplot(ratio, labels=labels, cmap=args['color'])
                                else:
                                        ratio.plot(lw=3,ls=':',label=args['label'],color=args['color'])

                if 'xrotation' in args.keys(): plt.xticks(rotation=args['xrotation'])

                #ax.legend()
                plt.tight_layout()
                plt.legend(loc='best',fontsize='x-small',ncol=2,fancybox=True)#,bbox_to_anchor=(0.5, 1.05),ncol=3, fancybox=True, shadow=True)
                plt.savefig(f'{SSaveLocation}/{allkey}.pdf', dpi=200)
                #fig.close()
                plt.close()

                
