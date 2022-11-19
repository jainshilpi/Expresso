#!/usr/bin/env python
print('------- Making plots ----------')
import argparse
import yaml
from pathlib import Path
from modules.ExpressoPlotTools import alldictplot
from modules.ExpressoPlotTools import makeplots_fromdict
import os

parser = argparse.ArgumentParser(description='Plotter Options')
parser.add_argument("--HistoFolder","-oF"   , default='./', help = 'Path to the histo directory')
parser.add_argument("--SaveLocation","-oS"   , default='./', help = 'directory to save plots')
parser.add_argument("--PlotterScript","-plotter"   , default='No', help = 'plotterscript')
args = parser.parse_args()

try:
    split=args.PlotterScript.split('/')
    dump=split[0]+'/'+split[1]+'/'+"plots.yaml"
    print("A more detailed dump of your plotter is created in "+dump)
    print("You can use it to customize plots further!!")
    print("Basic plots are here: "+args.SaveLocation+'/plots/')
    os.system("python modules/dump_plotyaml.py "+args.PlotterScript+" >"+dump)

    path = Path(dump)
    with open(path) as stream:
        data = yaml.safe_load(stream)

    
    alldictplot(data,args.HistoFolder,args.SaveLocation+'/plots/',plotsetting='modules/plotsettings.yaml')
except:
    print("#######################################")
    print("ERROR! Is the plotter script in the analysis folder?")
    print("ERROR! Or maybe you are supplying incorret format??")
    print("example plotter should look something like this:")
    print("#-----------------------------------")
    print("2016:")
    print("######## format samplename: filename,color,stack(nostack),scale")
    print("Higgs2tt: H2TTT_passoptions.pkl.gz,red,stack,1")
    print("Higgs2ttg: H2TTTG_passoptions.pkl.gz,green,stack,1")
    print("DYJ2LL50: DYJTLL50_passoptions.pkl.gz,blue,stack,1")
    print("DYJ2LL10t50: DYJTLL10T50_passoptions.pkl.gz,yellow,stack,1")
    print("plots:")
    print("######## format plottype_ref: axisname")
    print("normal_pt: Electron_pt")
    print("normal_eta: Electron_eta")
    print("#-----------------------------------")
    print("Check examples in other analysis")
