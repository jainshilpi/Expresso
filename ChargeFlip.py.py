#!/usr/bin/env python
# coding: utf-8

# In[1]:


files='/eos/cms/store/group/phys_egamma/akapoor/ChargeMisID/newsamples/*.root'


# In[2]:


import ROOT
import os
ROOT.gStyle.SetPalette(55)
ROOT.gStyle.SetOptStat(0); 
ROOT.gStyle.SetTextFont(42)


# In[3]:


#ROOT.ROOT.EnableImplicitMT()


# In[4]:


#header_path = "/eos/user/a/akapoor/SWAN_projects/ChargeMisID_ttH/ChargeFlipStudies/Analysis_python.h"
 
#ROOT.gInterpreter.Declare(f'#include <{header_path}>')

ROOT.gInterpreter.Declare('''
using Vec_t = const ROOT::RVec<float>&;
float ComputeInvariantMass(Vec_t pt, Vec_t eta, Vec_t phi, Vec_t mass) {
    const ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], mass[0]);
    const ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], mass[1]);
    return (p1 + p2).M();
}
float SumpT(Vec_t pt) {
    return (pt[0] + pt[1]);
}
''')


# In[5]:


def selection_2el2mu(df):
    df = df.Filter("nElectron==2", "Exactly two electrons")
    df = df.Define("GoodElectrons", "(Electron_pt > 10) && (Electron_mvaTTH > 0.8) && (Electron_cutBased > 2)")
    df = df.Filter("Sum(GoodElectrons) == 2","Exactly two good electrons")
    #df = df.Define("SortedElectronpT","Take(Electron_pt, Argsort(Electron_pt))")
    #df = df.Define("SortedElectroneta","Take(Electron_eta, Argsort(Electron_pt))")
    #df = df.Define("SortedElectronphi","Take(Electron_phi, Argsort(Electron_pt))")
    #df = df.Define("SortedElectronmass","Take(Electron_mass, Argsort(Electron_pt))")
    df = df.Define("NGoodElectrons", "Sum(GoodElectrons)")
    df = df.Define("Dielectron_mass", 
                   "ComputeInvariantMass(Electron_pt[GoodElectrons], Electron_eta[GoodElectrons], Electron_phi[GoodElectrons], Electron_mass[GoodElectrons])")
    df = df.Filter("(Dielectron_mass<111) && (Dielectron_mass>71)","Z mass cut")
    df = df.Define("SumpT", "SumpT(Electron_pt[GoodElectrons])")
    
    return df


# In[6]:


df = ROOT.RDataFrame("Events", files)


# In[7]:


dfsel=selection_2el2mu(df)


# In[8]:


report = dfsel.Report()


# In[9]:


report.Print()


# In[10]:





# In[11]:


def savehist(h=[],col=[],op="l"):
    
    c = ROOT.TCanvas("c", "", 800, 700)
    
    pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1);
    pad1.SetBottomMargin(0)
    pad1.Draw()
    pad1.cd()
    
    legend=ROOT.TLegend(0.5,0.8,0.9,0.9)
    
    h[0].GetXaxis().SetTitleSize(0.04)
    h[0].GetYaxis().SetTitleSize(0.02)
    
    h[0].SetLineColor(col[0])
    h[0].Draw("hist")
    legend.AddEntry(h[0].GetName(), h[0].GetName(), op)
    if len(h)>1:
        for i,hi in enumerate(h):
            if i!=0:
                h[i].SetLineColor(col[i])
                h[i].Draw("histsame")
                legend.AddEntry(h[i].GetName(), h[i].GetName(), op)
    legend.Draw()
    legend.SetTextSize(0.04)
    #h[0].SetAxisRange(h[0].GetMinimum(), 0.2*h[0].GetMaximum(), "Y");
    c.SaveAs((h[0].GetTitle())+".pdf")
    
    
def savehistwithratio(h=[],col=[],op="l"):
    if len(h)!=2:
        print("Only works with 2 hists")
        return 0;
    h1=h[0].Clone()
    h2=h[1].Clone()
    c1 = ROOT.TCanvas("c1","example",600,700);
    pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1);
    pad1.SetBottomMargin(0);
    pad1.Draw();
    pad1.cd();
    legend=ROOT.TLegend(0.5,0.8,0.9,0.9)
    
    h1.DrawCopy();
    h1.SetLineColor(col[0])
    legend.AddEntry(h1.GetName(), h1.GetName(), op)
    h2.Draw("same");
    h2.SetLineColor(col[1])
    legend.AddEntry(h2.GetName(), h2.GetName(), op)
    legend.Draw()
    legend.SetTextSize(0.04)
    
    c1.cd();
    
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.3);
    pad2.SetTopMargin(0);
    pad2.Draw();
    pad2.cd();
    h1.Sumw2();
    h1.SetStats(0);
    h1.Divide(h2);
    #h1.SetMarkerStyle(21);
    h1.SetMarkerSize(1)
    h1.Draw("text0 ep");
    c1.cd();
    
    c1.SaveAs((h[0].GetTitle())+".pdf")
    
    
def savehistonlyratio(h=[],col=[],op="l"):
    ROOT.gStyle.SetPaintTextFormat("4.4f");
    if len(h)!=2:
        print("Only works with 2 hists")
        return 0;
    h1=h[0].Clone()
    h2=h[1].Clone()
    c1 = ROOT.TCanvas("c1","example",600,700);
    legend=ROOT.TLegend(0.5,0.8,0.9,0.9)
    
    h1.Sumw2();
    h1.SetStats(0);
    h1.Divide(h2);
    #h1.SetMarkerStyle(21);
    h1.SetMarkerSize(1)
    h1.Draw("text0 ep");
    c1.SaveAs((h[0].GetTitle())+"_ratio.pdf")


# In[ ]:





# In[12]:


dfos=dfsel.Filter("Sum(Electron_charge)==0", "Two OS")


# In[13]:


report = dfos.Report()


# In[14]:


report.Print()


# In[15]:


def BookHisto(df,Args,Branch):
    return df.Histo1D(Args, Branch)


# In[16]:


h1 = dfsel.Filter("Sum(Electron_charge)==0", "Two OS").Histo1D(("Dielectron_mass_OS", "Dielectron_mass;m_{ee} (GeV);Events", 300, 71, 111), "Dielectron_mass")
h2 = dfsel.Histo1D(("Dielectron_mass_all", "Dielectron_mass;m_{ee} (GeV);Events", 300, 71, 111), "Dielectron_mass")

hSumpT= BookHisto(dfos,("SumpT", "SumpT_OS;pT_{e1}+pT_{e2} (GeV);Events", 1000, 0, 1000),"SumpT")
hNel= BookHisto(dfos,("NGoodElectrons", "NGoodElectrons;N_{el} (GeV);Events", 3, -0.5, 2.5),"NGoodElectrons")


# In[ ]:





# In[17]:


savehist([hSumpT,h1,h2],
         [ROOT.kRed,ROOT.kBlue,ROOT.kGreen])

savehist([hNel],
         [ROOT.kRed])

savehistwithratio([h1,h2],
         [ROOT.kRed,ROOT.kBlue])


# In[18]:


dfos.Report().Print()


# In[19]:


dfsel=dfsel.Define("LeadingGoodElectronpT", "Electron_pt[0]")
dfsel=dfsel.Define("SubLeadingGoodElectronpT", "Electron_pt[1]")

h1 = dfsel.Filter("Sum(Electron_charge)!=0", "Two SS").Histo1D(("Electron_pt_SS", "Electron_pt;Electron_pt (GeV);Events", 5, 0, 100), "LeadingGoodElectronpT")
h2 = dfsel.Histo1D(("Electron_pt_all", "Electron_pt;Electron_pt;Events", 5, 0, 100), "LeadingGoodElectronpT")
savehistonlyratio([h1,h2],
                  [ROOT.kRed,ROOT.kBlue])

h1 = dfsel.Filter("Sum(Electron_charge)!=0", "Two SS").Histo1D(("SubElectron_pt_SS", "SubElectron_pt;SubElectron_pt (GeV);Events", 5, 0, 100), "SubLeadingGoodElectronpT")
h2 = dfsel.Histo1D(("SubElectron_pt_all", "SubElectron_pt;SubElectron_pt;Events", 5, 0, 100), "SubLeadingGoodElectronpT")
savehistonlyratio([h1,h2],
                  [ROOT.kRed,ROOT.kBlue])



savehistwithratio([dfsel.Histo1D(("Electron_pt_all", "Electron_pt;Electron_pt;Events", 5, 0, 100), "LeadingGoodElectronpT"),
                   dfsel.Histo1D(("SubElectron_pt_all", "SubElectron_pt;SubElectron_pt;Events", 5, 0, 100), "SubLeadingGoodElectronpT")],
                  [ROOT.kRed,ROOT.kBlue])


# In[20]:


#import pandas
#df=pandas.DataFrame(dfsel.AsNumpy())


# In[21]:


#df.head()


# In[22]:





# In[ ]:




