import gzip
try:
        import pickle5 as pickle
except ImportError:
        import pickle
#import hist
import coffea.hist as hist
from tabulate import tabulate
import matplotlib.pyplot as plt
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

def dictplotratio(histodict,outputfolder,SSaveLocation):
    
    for hiname in histodict.keys():
        histo=histodict[hiname]
        fig, ax = plt.subplots()
        hep.style.use('CMS')
        hep.cms.label('', data=False)
        for k in histo.keys():
                

                dicty1=histo[k][0]
                dicty2=histo[k][1]
                #print(dicty1)
                #print(dicty2)
                
                try:
                        h1=get_hist_from_pkl(outputfolder+'/'+dicty1['file'])[dicty1['label']].project(dicty1['axis'])
                        h2=get_hist_from_pkl(outputfolder+'/'+dicty2['file'])[dicty2['label']].project(dicty2['axis'])
                        hist.plotratio(
                                num=h2,
                                denom=h1,
                                clear=False,
                                error_opts={'color': histo[k][2]['color'], 'marker': '.'},
                                unc='num',ax=ax,label=dicty1['label'])
                except:
                        h1=get_hist_from_pkl(outputfolder+'/'+dicty1['file'])[dicty1['label']].to_hist().project(dicty1['axis'])
                        h2=get_hist_from_pkl(outputfolder+'/'+dicty2['file'])[dicty2['label']].to_hist().project(dicty2['axis'])
                        ###### Print ratios with erros
                        ratio = (h2/h1)
                        err_up, err_down = ratio_uncertainty(h2.values(), h1.values(), 'poisson-ratio')
                        labels = []                        
                        for ra, u, d in zip(ratio.values().ravel(), err_up.ravel(), err_down.ravel()):
                                ra, u, d = f'{ra:.6f}', f'{u:.6f}', f'{d:.6f}'
                                st = '$'+ra+'_{-'+d+'}^{+'+u+'}$'
                                labels.append(st)
                        labels = np.array(labels)#.reshape(ratio.values().shape)
                        data=[]
                        with open(f'{SSaveLocation}/{hiname}_ratio.txt', 'w') as fi:
                                for i in range(len((h2/h1).view())):
                                        data.append([(h2/h1).axes[0][i],labels[i]]) 
                                fi.write(tabulate(data, headers=["Bin", "Value"]))
                                
                               #fi.write(f'\"{(h2/h1).axes[0][i]}\" : {labels[i]}')
                               #fi.write('\n')
                        ###### Print ratios with erros
                        (h2/h1).plot(ax=ax, lw=3,
                                     label=dicty1['label'],
                                     #labels=labels,
                                     color=histo[k][2]['color'])
                        plt.xticks(rotation=90,fontsize=7)
                #(h2/h1).plot(ax=ax, lw=3,label=dicty1['label'])
                ax.legend()
                fig.tight_layout()
                plt.legend(loc='best')
                plt.savefig(f'{SSaveLocation}/{hiname}_ratio.pdf', dpi=200)

def dictplot2Dratio(histodict,outputfolder,SSaveLocation):
    
    for hiname in histodict.keys():
        histo=histodict[hiname]
        dicty1=histo[0]
        dicty2=histo[1]
        x1=dicty1['xaxis']
        y1=dicty1['yaxis']
        x2=dicty2['xaxis']
        y2=dicty2['yaxis']
        h1=get_hist_from_pkl(outputfolder+'/'+dicty1['file'])[dicty1['label']].project(y1,x1)
        h2=get_hist_from_pkl(outputfolder+'/'+dicty2['file'])[dicty2['label']].project(y2,x2)
        ratio = (h1.to_hist()/h2.to_hist())
        #print(ratio)
        #print(ratio.values().shape)
        err_up, err_down = ratio_uncertainty(h1.to_hist().values(), h2.to_hist().values(), 'poisson-ratio')
        labels = []
        for ra, u, d in zip(ratio.values().ravel(), err_up.ravel(), err_down.ravel()):
                ra, u, d = f'{ra:.6f}', f'{u:.6f}', f'{d:.6f}'
                st = '$'+ra+'_{-'+d+'}^{+'+u+'}$'
                labels.append(st)
        #print(labels)
        labels = np.array(labels).reshape(ratio.values().shape)
        with open(f'{SSaveLocation}/{hiname}_2Dratio.txt', 'w') as fi:
                fi.write(f'{labels}')
        fig, ax = plt.subplots(figsize=tuple([z * 20 for z in ratio.values().shape]))
        hep.style.use('CMS')
        hep.cms.label('', data=False)
        hep.hist2dplot(ratio, labels=labels, cmap='plasma',ax=ax)
        #ax.tick_params(labelsize=10)
        #hist.plot2d(hist=ratio,xaxis=x1,ax=ax,clear=True)
        ax.legend()
        fig.tight_layout()
        plt.legend(loc='best')
        plt.savefig(f'{SSaveLocation}/{hiname}_2Dratio.pdf', dpi=200)
                
def dictplotnormal(histodict,outputfolder,SSaveLocation):
    
            for hiname in histodict.keys():
                histo=histodict[hiname]
                fig, ax = plt.subplots()
                hep.style.use('CMS')
                hep.cms.label('', data=False)
                nostack=[]
                stack=[]
                nostacklabels=[]
                stacklabels=[]
                for k in histo.keys():
                    dicty=histo[k]
                    scale=1.0
                    if 'scale' in histo[k].keys():
                        scale=histo[k]['scale']
                        
                    thist=get_hist_from_pkl(outputfolder+"/"+histo[k]['file'])[k]
                    thist.scale(scale)
                    #print(thist)
                    histo[k]['h']=thist.to_hist().project(histo[k]['axis'])
                    #print(histo[k]['h'].project(histo[k]['axis']))
                    #print(histo[k]['axis'])
                    if(histo[k]['stack']==True):
                        stack.append(histo[k]['h'])
                        stacklabels.append(histo[k]['label'])
                    if(histo[k]['stack']==False):
                        nostack.append(histo[k]['h'])
                        nostacklabels.append(histo[k]['label'])
                if len(stack)!=0:
                        hep.histplot(stack,ax=ax,lw=3,stack=True,histtype='fill',label=stacklabels)
                if len(nostack)!=0:
                        hep.histplot(nostack,ax=ax,lw=3,stack=False,histtype='step',label=nostacklabels, yerr=True)
                ax.tick_params(axis="x")
                if 'cutflow' in histo[k]['axis']: plt.xticks(rotation=45)
                if 'selection' in histo[k]['axis']: plt.xticks(rotation=45)
                ax.legend()
                fig.tight_layout()
                plt.legend(loc='best')
                plt.savefig(f'{SSaveLocation}/{hiname}_normal.pdf', dpi=200)
                #print(histo[k]['axis']+'_check')


def dictplot(histodictall,outputfolder,SaveLocation='./'):
        import os
        SSaveLocation=SaveLocation
        if SaveLocation=='./': SSaveLocation='plots'
        os.system(f'mkdir -p {SSaveLocation}')
        for allkey in histodictall.keys():
                if allkey=='normal': dictplotnormal(histodictall[allkey],outputfolder,SSaveLocation)
                if allkey=='ratio': dictplotratio(histodictall[allkey],outputfolder,SSaveLocation)
                if allkey=='2Dratio': dictplot2Dratio(histodictall[allkey],outputfolder,SSaveLocation)

                
