from modules.ExpressoPlotter import ExpressoPlotter,normalplot
import coffea, uproot3, numpy
from modules.ExpressoPlotter import ExpressoPlotter,normalplot

#Output/Analysis/HiggsToZG/output/analysis/GluGluHToZG.pkl.gz
plotter=ExpressoPlotter("2017")
plotter.histolocation('Output/Analysis/HiggsToZG/output/analysis/')
plotter.savelocation('./')
plotter.settings('modules/plotsettings.yaml')

#plotter.addfile('ggH','GluGluHToZG.pkl.gz','red','nostack',-1)
#plotter.addfile('ggH','Zgamma.pkl.gz','blue','nostack',-1)

plotter.addfile('ggH','GluGluHToZG.pkl.gz','red','nostack',1)
#plotter.addfile('Zg','Zgamma.pkl.gz','blue','nostack',1)
#plotter.addfile('Zjets','Zjets.pkl.gz','green','nostack',1)

#plotter.addfile('test1','test_anap_tight.pkl.gz','blue','stack',-1)
#plotter.addfile('test2','test_anap_tight.pkl.gz','green','stack',2)

#p=normalplot(plotter,filename="sumw",hi='sumw',axis='sumw')
#p=normalplot(plotter,filename="Nele",hi='Nele',axis='Nele')
p=normalplot(plotter,filename="Meeg",hi='Meeg',axis='Meeg')
p=normalplot(plotter,filename="Mmmg",hi='Mmmg',axis='Mmmg')
p=normalplot(plotter,filename="Mttg",hi='Mttg',axis='Mttg')


'''
coffea_h=plotter.getcoffeahist('ggH','Mmmg')
#### now starts the magic
fout = uproot3.recreate('ggH.root')
fout['Mmmg'] = coffea.hist.export1d(coffea_h.project('Mmmg'))
fout['Meeg'] = coffea.hist.export1d(coffea_h.project('Meeg'))
fout['Mttg'] = coffea.hist.export1d(coffea_h.project('Mttg'))
fout.close()


coffea_h=plotter.getcoffeahist('Zg','Mmmg')
#### now starts the magic
fout = uproot3.recreate('Zg.root')
fout['Mmmg'] = coffea.hist.export1d(coffea_h.project('Mmmg'))
fout['Meeg'] = coffea.hist.export1d(coffea_h.project('Meeg'))
fout['Mttg'] = coffea.hist.export1d(coffea_h.project('Mttg'))
fout.close()


coffea_h=plotter.getcoffeahist('Zjets','Mmmg')
#### now starts the magic
fout = uproot3.recreate('Zjets.root')
fout['Mmmg'] = coffea.hist.export1d(coffea_h.project('Mmmg'))
fout['Meeg'] = coffea.hist.export1d(coffea_h.project('Meeg'))
fout['Mttg'] = coffea.hist.export1d(coffea_h.project('Mttg'))
fout.close()

'''
