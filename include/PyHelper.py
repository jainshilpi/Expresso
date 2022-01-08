
import ROOT
def Clone(h):
    htemp=h[:]
    h=[]
    for hi in htemp:
        h.append(hi.Clone())
    return h

def prepareevents(Process,Aliases,Definitions,Selections):
    import ROOT
    PDs=[]
    for cont in Process.keys():
        Files=Process[cont]['Files']
        Tree=Process[cont]['Tree']
        df = ROOT.RDataFrame(Tree, Files)
        for define in Definitions.keys():
            df = df.Define(define,Definitions[define])
        for alias in Aliases.keys():
            df = df.Alias(alias,Aliases[alias])
        for sel in Selections.keys():
            df = df.Filter(sel,Selections[sel])
        PDs.append({'cont':cont,'Type':Process[cont]['Type'],'RDF':df,'Xsec':Process[cont]['Xsec']})
    return PDs

def savehist(h=[],col=[],op="l",norm=False):
    h=Clone(h)
    c = ROOT.TCanvas("c","example",600,700);
    #pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1);
    #pad1.SetBottomMargin(0)
    #pad1.Draw()
    #pad1.cd()
    #ROOT.gPad.SetLogy()
    legend=ROOT.TLegend(0.5,0.8,0.9,0.9)
    
    if norm: h[0].Scale(1/h[0].Integral());
    #h[0].GetXaxis().SetTitleSize(0.04)
    #h[0].GetYaxis().SetTitleSize(0.02)
    
    h[0].SetLineColor(col[0])
    h[0].Draw("hist")
    legend.AddEntry(h[0].GetName(), h[0].GetName(), op)
    if len(h)>1:
        for i,hi in enumerate(h):
            if i!=0:
                if norm: h[i].Scale(1/h[i].Integral());
                h[i].SetLineColor(col[i])
                h[i].Draw("histsame")
                legend.AddEntry(h[i].GetName(), h[i].GetName(), op)
    legend.Draw()
    legend.SetTextSize(0.02)
    #h[0].SetAxisRange(h[0].GetMinimum(), 0.2*h[0].GetMaximum(), "Y");
    if norm: c.SaveAs((h[0].GetTitle())+"_norm.pdf")
    if not norm: c.SaveAs((h[0].GetTitle())+".pdf")
    
    
def savehistwithratio(h=[],col=[],op="l"):
    h=Clone(h)
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
    h=Clone(h)
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
    h1.Divide(h2)
    #h1.SetMarkerStyle(21);
    h1.SetMarkerSize(1)
    h1.Draw("text0 ep");
    c1.SaveAs((h[0].GetTitle())+"_ratio.pdf")
    
def BookHisto(df,Args,Branch):
    return df.Histo1D(Args, Branch)