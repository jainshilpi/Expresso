import gzip
import pickle
import hist
import matplotlib.pyplot as plt
import mplhep as hep

def get_hist_from_pkl(path_to_pkl,allow_empty=True):
        h = pickle.load( gzip.open(path_to_pkl) )
        if not allow_empty:
            h = {k:v for k,v in h.items() if v.values() != {}}
        return h


def dictprint(di):
        for key, value in di.items():
                print(key, ' : ', value)

def dictplotnormal(histodict,outputfolder):
    
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
                    #histo[k]['h']=get_hist_from_pkl(histo[k]['file'])[k].to_hist().project(histo[k]['axis'])
                    histo[k]['h']=thist.to_hist().project(histo[k]['axis'])
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
                plt.legend(loc='best')
                plt.savefig(f'{outputfolder}/{hiname}.pdf', dpi=200)


def dictplot(histodictall,outputfolder):
    
    for allkey in histodictall.keys():
        if allkey=='normal':
            dictplotnormal(histodictall[allkey],outputfolder)

                
