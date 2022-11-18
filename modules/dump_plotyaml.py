'''

Dumper script

pass a simple yaml file like this
-------------------------------------
2016:
    ######## format samplename: filename,color,stack(nostack),scale
    Higgs2tt: H2TTT_passoptions=Xsecweight.pkl.gz,red,stack,1
    Higgs2ttg: H2TTTG_passoptions=Xsecweight.pkl.gz,green,stack,1
    DYJ2LL50: DYJTLL50_passoptions=Xsecweight.pkl.gz,blue,stack,1
    DYJ2LL10t50: DYJTLL10T50_passoptions=Xsecweight.pkl.gz,yellow,stack,1
plots:
    ######## format plottype_ref: axisname
    normal_pt: Electron_pt
    normal_eta: Electron_eta

-------------------------------------

Get it converted to full form yaml
python modules/dump_plotyaml.py allplots.yaml > plot.yaml

Then pass it to plot+.py

'''
import yaml
import pprint
import sys

input_condensed=sys.argv[1]

with open(input_condensed) as file:
    try:
        Config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)
plotyaml={}

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

print(yaml.dump(plotyaml,default_flow_style=False))
