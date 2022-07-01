#!/usr/bin/env python
import argparse
parser = argparse.ArgumentParser(description='Plotter Options')
parser.add_argument("--HistoFolder","-oF"   , default='./', help = 'Path to the histo directory')
parser.add_argument("--SaveLocation","-oS"   , default='./', help = 'directory to save plots')
parser.add_argument("--PlotterScript","-plotter"   , default='No', help = 'plotterscript')
args = parser.parse_args()
#-------------------------------------------------------------------------------------------
import importlib
plotter = importlib.import_module(f'{args.PlotterScript.replace(".py","").replace("/",".")}')
from modules.ExpressoPlotTools import dictplot
dictplot(plotter.histodict,args.HistoFolder,args.SaveLocation)
