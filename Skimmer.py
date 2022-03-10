#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import os

if hasattr(__builtins__,'__IPYTHON__'):
    sysName='DY'
    sysfiles='/eos/cms/store/group/phys_egamma/akapoor/ChargeMisID/newsamples2/06544C90-EFDF-E811-80E6-842B2B6F5D5C.root'
    saveRootFile=True
    outfolder='Output'
    outsuffix='1'
    debugprint=True
    analysis='Ana/TTH'
    multithreaded=False
    xsec=1.00
    istype='mc'
    #!python3 -m pip install correctionlib
    path = '/eos/user/a/akapoor/.local/bin'
    os.environ['PATH'] += ':'+path
    #branchlist="(ChargeFlip_Category|MyElectron_pt)"
else:
    parser = argparse.ArgumentParser(description='Options for the analyzer')
    parser.add_argument('--name', metavar='n', action='store', type=str,help='short name of the physics process/Data sample', required=True)
    parser.add_argument('--file', metavar='f', action='store', type=str,help='location of files',required=True)
    parser.add_argument('--saveroot',action='store_true', help='save root file',default=False)
    parser.add_argument('--debugprint',action='store_true', help='print analysis settings for debug',default=False)
    parser.add_argument('--outfolder', metavar='of', action='store', type=str,help='location of output',default='Output',required=True)
    parser.add_argument('--outsuffix', metavar='os', action='store', type=str,help='suffix to recognize job',default='Output')
    parser.add_argument('--analysis', metavar='ana', action='store', type=str,help='Folder name that has analysis configs',default='Output',required=True)
    parser.add_argument('--multithreaded', action='store_true', help='mt',default=False)
    parser.add_argument('--xsec', metavar='xsec', action='store', type=float, help='xsec',default=1,required=True )
    parser.add_argument('--istype', metavar='istype', action='store', type=str, help='data or mc',default='mc',required=True )
    #parser.add_argument('--branchlist', metavar='bl', action='store', type=str,help='branches to store in skim',default="(MyElectron_eta|MyElectron_pt)")
    args = parser.parse_args()
    
    sysName=str(args.name)
    sysfiles=str(args.file)
    saveRootFile=args.saveroot
    outfolder=str(args.outfolder)
    outsuffix=str(args.outsuffix)
    analysis=str(args.analysis)
    debugprint=args.debugprint
    multithreaded=args.multithreaded
    xsec=args.xsec
    istype=args.istype
    #branchlist=str(args.branchlist)

os.system("mkdir OutputFiles")    
os.system("mkdir OutputFiles/"+outfolder)
outfolder="OutputFiles/"+outfolder


# In[2]:


import ROOT
if multithreaded:
    ROOT.ROOT.EnableImplicitMT()

#ROOT.gROOT.ProcessLine(".L /correctionlib/correctionlib/include/_core.cpython-38-x86_64-linux-gnu.so");
#ROOT.gSystem.Load('_core.cpython-38-x86_64-linux-gnu.so')
ROOT.gInterpreter.AddIncludePath("./include/modules/");
#ROOT.gInterpreter.AddIncludePath("./correctionlib/correctionlib/include/");


# In[3]:


import glob
modules = [os.path.basename(x) for x in glob.glob('./include/modules/*.h')]


# In[4]:


print(f"Loading modules {modules}")


# In[5]:


for mo in modules:
    ROOT.gInterpreter.ProcessLine('#include "'+mo+'"')
#ROOT.gInterpreter.ProcessLine('#include "correction.h"')

from include.PyHelper import *


# In[6]:


import yaml
ObjectCutsFile=analysis+"/ObjectCuts.yaml"
DefinitionsFile=analysis+"/Definitions.yaml"
SelectionsFile=analysis+"/Selections.yaml"
BranchesToSaveFile=analysis+"/BranchesToSave.yaml"
WeightConfig=analysis+"/WeightConfig.yaml"
ApplyWeights=analysis+"/ApplyWeights.yaml"
Histostosave=analysis+"/Histos.yaml"


# In[ ]:





# In[7]:


ObjectCuts = yaml.safe_load(open(ObjectCutsFile, 'r'))
Definitions = yaml.safe_load(open(DefinitionsFile, 'r'))
Selections = yaml.safe_load(open(SelectionsFile, 'r'))
BranchesToSave = yaml.safe_load(open(BranchesToSaveFile, 'r'))
WeightConfig = yaml.safe_load(open(WeightConfig, 'r'))
ApplyWeights = yaml.safe_load(open(ApplyWeights, 'r'))
Histos=yaml.safe_load(open(Histostosave, 'r'))


# In[ ]:





# In[8]:


def listtostdvector(mylist):
    mynewList = ROOT.std.vector('std::string')()
    for element in mylist:
        mynewList.push_back(element)
    return mynewList


# In[9]:


import sys
if saveRootFile:
    if BranchesToSave is None:
        sys.exit('\033[91m'+"saving a root file is not supported without list of branches to save"+'\033[0m')


# In[ ]:





# In[10]:


import correctionlib
correctionlib.register_pyroot_binding()

Ana= MyAnalyzer()
if ObjectCuts is not None:
    for key in ObjectCuts.keys():
        exec(f'{key}mask=ObjectMask()')
        for cut in ObjectCuts[key]:
            exec(f'{key}mask.addcut("{cut}")')
        exec(f'mask={key}mask.mask')
        exec(f'Ana.definition("{key}",{key}mask.mask)')

if Definitions is not None:
    for key in Definitions.keys():
        Ana.definition(key,Definitions[key])
        
if Selections is not None:
    for key in Selections.keys():
        Ana.sel(key,Selections[key])
        
if WeightConfig is not None:
    for corr in WeightConfig:
        ROOT.gInterpreter.Declare(corr)
        
if ApplyWeights is not None:
    for key in ApplyWeights:
        Ana.definition(key,ApplyWeights[key])
    
    
processname=sysName
processdict={'Files':sysfiles,'Type':istype,'Tree':'Events','Xsec':xsec}
Ana.process(processname,processdict)


# In[11]:


Total=Ana.prepare()


# In[12]:


DF=Ana.PD[sysName]['RDF']


# In[ ]:





# In[13]:


import json
if debugprint:
    
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print('Dumping the analysis graph')
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print(f'Object Mask Cuts from {ObjectCutsFile}')
    print(json.dumps(ObjectCuts, indent=3))
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print(f'All the definitions from {DefinitionsFile}')
    print(json.dumps(Definitions, indent=3))
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print(f'All the Event Selections from {SelectionsFile}')
    print(json.dumps(Selections, indent=3))
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print(f'Sample information provided as options')
    print(json.dumps(processdict, indent=3))
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print(f'Branches to save taken from {BranchesToSaveFile}')
    print(json.dumps(BranchesToSave, indent=3))
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print(f'Weight Config')
    print(json.dumps(WeightConfig, indent=3))
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print(f'Weights avilable')
    print(json.dumps(ApplyWeights, indent=3))
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    print(f'Histograms that will be saved')
    print(json.dumps(Histos, indent=3))
    print('---------------------------------------------------')
    print('---------------------------------------------------')
    if not hasattr(__builtins__,'__IPYTHON__'):
        print('Skimmer options used')
        print(args)
    print('---------------------------------------------------')
    print('---------------------------------------------------')


# In[14]:


#DF.Display({"event","elpt","eldeepjet"}).Print()
cutflow=DF.Report()
Final=DF.Count()
hists=[]
if Histos is not None:
    for hist in Histos:
        hists.append(DF.Histo1D(hist))


# In[15]:


print('Saving the Action Graph')
ROOT.RDF.SaveGraph(cutflow, f'{outfolder}/ActionGraph.dot')
from graphviz import render
render('dot', 'png', f'{outfolder}/ActionGraph.dot')


# In[16]:


import sys

if saveRootFile:
    #BRS=BranchesToSave.replace(" ", "")
    outfilenow=outfolder+"/output_"+outsuffix+".root"
    if BranchesToSave is not None:
        snapshot=DF.Snapshot("Events",outfilenow,listtostdvector(BranchesToSave))
    #fdf=DF.Snapshot("Events",outfilenow,f"{BRS}")
    #if debugprint:
    cutflow.Print()
    #sys.stdout = open(outfolder+"/CutFlow.csv", "a")
    #print(f'{sysfiles}' + "\n")
    
    #sys.stdout.close()
    TotalEvents=Total.GetValue()
    FinalEvents=Final.GetValue()
    with open(outfolder+"/Info.csv", "a") as text_file:
            #print(driver.current_url)
            text_file.write(f'{sysfiles}, {istype}, {xsec}, {FinalEvents}, {TotalEvents}, {round((FinalEvents*100)/TotalEvents,2)}%, {outfilenow}' + "\n")


# In[ ]:





# In[18]:


if saveRootFile:
        if BranchesToSave is not None:    
            f = ROOT.TFile(outfilenow,"update")
            for histi in hists:
                histi.Sumw2()
                histi.Write()
            f.Close()
            


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




