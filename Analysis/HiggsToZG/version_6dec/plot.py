from modules.ExpressoPlotter import ExpressoPlotter,normalplot

#Output/Analysis/HiggsToZG/output/analysis/GluGluHToZG.pkl.gz
plotter=ExpressoPlotter("2017")
plotter.histolocation('Output/Analysis/HiggsToZG/output/analysis/')
plotter.savelocation('./')
plotter.settings('modules/plotsettings.yaml')

plotter.addfile('ggH','GluGluHToZG.pkl.gz','red','nostack',-1)
#plotter.addfile('test1','test_anap_tight.pkl.gz','blue','stack',-1)
#plotter.addfile('test2','test_anap_tight.pkl.gz','green','stack',2)

#p=normalplot(plotter,filename="sumw",hi='sumw',axis='sumw')
#p=normalplot(plotter,filename="Nele",hi='Nele',axis='Nele')
p=normalplot(plotter,filename="Meeg",hi='Meeg',axis='Meeg')
p=normalplot(plotter,filename="Mmmg",hi='Mmmg',axis='Mmmg')
p=normalplot(plotter,filename="Mttg",hi='Mttg',axis='Mttg')
