#!/usr/bin/env python
print('------- Making plots ----------')
import argparse
import yaml
from pathlib import Path
from modules.ExpressoPlotTools import alldictplot

parser = argparse.ArgumentParser(description='Plotter Options')
parser.add_argument("--HistoFolder","-oF"   , default='./', help = 'Path to the histo directory')
parser.add_argument("--SaveLocation","-oS"   , default='./', help = 'directory to save plots')
parser.add_argument("--PlotterScript","-plotter"   , default='No', help = 'plotterscript')
args = parser.parse_args()

path = Path(args.PlotterScript)
with open(path) as stream:
    data = yaml.safe_load(stream)


alldictplot(data,args.HistoFolder,args.SaveLocation+'/plots/',plotsetting='modules/plotsettings.yaml')
