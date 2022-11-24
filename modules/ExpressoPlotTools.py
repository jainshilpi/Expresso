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
from hist.intervals import ratio_uncertainty, clopper_pearson_interval, poisson_interval
import numpy as np
def get_hist_from_pkl(path_to_pkl,allow_empty=True):
        h = pickle.load( gzip.open(path_to_pkl) )
        if not allow_empty:
            h = {k:v for k,v in h.items() if v.values() != {}}
        return h

def geths(h,scale=-1):
        if scale==-1:
                return h*(1/sum(list(h.counts())))
        else:
                return h*scale

def dictprint(di):
        for key, value in di.items():
                print(key, ' : ', value)

def geterrratio(hi,typeunc='p'):
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
                if os.path.exists(f'{SSaveLocation}/{allkey}.txt'):
                        os.remove(f'{SSaveLocation}/{allkey}.txt')

                histodict=histodictall[allkey]
                
                if ps['hepstyle']=='ROOT':
                        hep.style.use(hep.style.ROOT)
                if ps['hepstyle']=='CMS':
                        hep.style.use("CMS")
                        hep.cms.label(ps["PrivateLabel"], data=ps["withdata"], year=year)
                        
                if 'normal' in allkey:
                        nostack=[]
                        stack=[]
                        nostacklabels=[]
                        nostackcolors=[]
                        stacklabels=[]
                        stackcolors=[]
                        stackscales=[]
                        nostackscales=[]
                if 'ratio' in allkey and '2D' not in allkey:
                        fig, ax = plt.subplots()
                        
                for hiname in histodict.keys():
                        histo=histodict[hiname]

                        print(f'---{hiname}---')
                        
        
                        if 'args' in histo.keys():
                                args=histo['args']
                                del histo['args']
                                
                        for k in histo.keys():
                                print(f'{k}')
                                thist=get_hist_from_pkl(outputfolder+"/"+files[histo[k]['file']])[k]
                                if '2Dratio' in allkey:
                                        histo[k]['h']=thist.project(histo[k]['xaxis'],histo[k]['yaxis'])
                                else:
                                        histo[k]['h']=(thist).project(histo[k]['axis'])
                                        
        
        
                        if 'normal' in allkey:
                                for k in histo.keys():
                                        #if k == 'args': continue
                                        if(histo[k]['stack']==True):
                                                stack.append(histo[k]['h'])
                                                stacklabels.append(args['label'])
                                                stackcolors.append(args['color'])
                                                stackscales.append(histo[k]['scale'])
                                        if(histo[k]['stack']==False):
                                                nostack.append(histo[k]['h'])
                                                nostacklabels.append(args['label'])
                                                nostackcolors.append(args['color'])
                                                nostackscales.append(histo[k]['scale'])
                    
                        if 'ratio' in allkey:
                                hi=[]
                                hic=[]
                                #print(histo.keys())
                                for i,k in enumerate(histo.keys()):
                                        #if k == 'args': continue
                                        hi.append(histo[k]['h'].to_hist())
                                        hic.append(histo[k]['h'])
                                #ratio = (hi[0].view()/hi[1].view())
                                ratio,labels=geterrratio(hi,typeunc='p')
                                print('------eff---------')
                                print(labels)
                                ratio,labels=geterrratio(hi)
                                print('------CP---------')
                                print(labels)
                                if '2D' in allkey:
                                        fig, ax = plt.subplots(figsize=tuple([z * 10 for z in ratio.shape]))
                                        labels = np.array(labels).reshape(ratio.shape)
                                        with open(f'{SSaveLocation}/{allkey}.txt', 'w') as fi:
                                                fi.write(f'{labels}')
                                else:
                                        labels = np.array(labels)
                                        data=[]
                                        with open(f'{SSaveLocation}/{allkey}.txt', 'a') as fi:
                                                for i in range(len((hi[0]).view())):
                                                        data.append([(hi[0]).axes[0][i],labels[i]])
                                                lab=args['label']
                                                fi.write("\n")
                                                fi.write(f'----{lab}----')
                                                fi.write("\n")
                                                fi.write(tabulate(data, headers=["Bin", "Value"]))
                                                fi.write("\n")
                                if '2D' in allkey:
                                        ybins=[i[0] for i in (hi[0]).axes[1]]
                                        ybins.append(hi[0].axes[1][-1][1])
                                        xbins=[(hi[0]).axes[0][i][0] for i in range(len((hi[0]).view()))]
                                        xbins.append((hi[0]).axes[0][len((hi[0]).view())-1][1])
                                        hep.hist2dplot(ratio, xbins=xbins,ybins=ybins,labels=labels, cmap=args['color'])
                                        #hist.plotratio(hi[0], xbins=xbins,ybins=ybins,labels=labels, cmap=args['color'])
                                else:
                                        bins=[(hi[0]).axes[0][i][0] for i in range(len((hi[0]).view()))]
                                        bins.append((hi[0]).axes[0][len((hi[0]).view())-1][1])
                                        #hep.histplot(ratio, bins=bins, color=args['color'], label=args['label'])
                                        color=f"tab:{args['color']}"
                                        hist.plotratio(hic[0],hic[1],ax=ax,
                                                       error_opts= {'linestyle': 'none','marker': '.'
                                                                    , 'markersize': 10.,'color': color,  'elinewidth': 1},
                                                       unc='clopper-pearson',
                                                       clear=False)

                if 'xrotation' in args.keys(): plt.xticks(rotation=args['xrotation'])

                if 'normal' in allkey:
                        if len(stack)!=0:
                                        hep.histplot([geths(st.to_hist(),scaleit) for st,scaleit in zip(stack,stackscales)],lw=1,stack=True,histtype='fill',label=stacklabels, color=stackcolors)
                        if len(nostack)!=0:
                                        hep.histplot([geths(nst.to_hist(),scaleit) for nst,scaleit in zip(nostack,nostackscales)],lw=1,stack=False,histtype='step',label=nostacklabels,
                                                     color=nostackcolors)

                #if 'normal' in allkey or '2D' in allkey:
                plt.tight_layout()
                plt.legend(loc='best',fontsize='x-small',ncol=2,fancybox=True)#,bbox_to_anchor=(0.5, 1.05),ncol=3, fancybox=True, shadow=True)
                plt.savefig(f'{SSaveLocation}/{allkey}.pdf', dpi=200)
                plt.close()

                

def makeplots_fromdict(plotyaml,HistoFolder,SaveLocation,plotsetting):

        ##################################3
        plotyaml['year']=list(Config.keys())[0]
        plotyaml['files']={}

        for sample in Config[plotyaml['year']].keys():
                plotyaml['files'][str(sample)]=Config[plotyaml['year']][sample].split(",")[0]

        for plot in Config['plots'].keys():
                plotyaml[plot]={}

                for i,sample in enumerate(Config[plotyaml['year']].keys()):
                        plotyaml[plot][str(i+1)]={}
                        stack=False
                        
                if (Config[plotyaml['year']][sample].split(",")[2]=='stack'): stack=True
                        
                color=Config[plotyaml['year']][sample].split(",")[1]

                scale=int(Config[plotyaml['year']][sample].split(",")[3])

                plotyaml[plot][str(i+1)][Config['plots'][plot]]={'axis':Config['plots'][plot],
                                                         'file': sample,'stack': stack,'scale':scale}
                plotyaml[plot][str(i+1)]['args']={'color':color,'label':sample}

        print('------- Making plots ----------')
        import argparse
        import yaml
        from pathlib import Path
