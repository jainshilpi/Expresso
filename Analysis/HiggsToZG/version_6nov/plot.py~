from modules.ExpressoPlotter import ExpressoPlotter,normalplot

plotter=ExpressoPlotter("2016")
plotter.histolocation('Output/Analysis/barebones/output/analysis/')
plotter.savelocation('./')
plotter.settings('modules/plotsettings.yaml')

plotter.addfile('test','test_anap_tight.pkl.gz','red','nostack',-1)
plotter.addfile('test1','test_anap_tight.pkl.gz','blue','stack',-1)
plotter.addfile('test2','test_anap_tight.pkl.gz','green','stack',2)

p=normalplot(plotter,filename="sumw",hi='sumw',axis='sumw')
p=normalplot(plotter,filename="Nele",hi='Nele',axis='Nele')
