#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "TSystem.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
 
using namespace ROOT;
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;

using Vec_t = const ROOT::RVec<float>&;
using RVecF = RVec<float>;
using RVecI = RVec<int>;

RVecF GenerateDecayTime(RVecI Particle_pid, RVecF Particle_px, RVecF Particle_py, RVecF Particle_pz, RVecF Particle_energy) {
    int countmesons=0;
    for (size_t i = 0; i < Particle_pid.size(); i++){
	if (Particle_pid[i]==4900111){
	    countmesons=countmesons+1;}
    }
    RVecI Particle_DecayTime(countmesons*2000);
    int iteration=0;
    for (size_t i = 0; i < Particle_pid.size(); i++){
	if (Particle_pid[i]==4900111){;
	    for (size_t k = iteration*2000; k < (iteration+1)*2000 ; k++){
		
		//Your exp generator
		Particle_DecayTime[k]=0;
		//////////
	    }
	    iteration=iteration+1;
	}
    }
    return Particle_DecayTime;
}
    
float ComputeInvariantMass(Vec_t pt, Vec_t eta, Vec_t phi, Vec_t mass) {
    const ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], mass[0]);
    const ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], mass[1]);
    return (p1 + p2).M();
}

float SumpT(Vec_t pt) {
    return (pt[0] + pt[1]);
}

float At(Vec_t pt,int n) {
    return (pt[n]);
}

float DeltaR(float eta1,float phi1,float eta2,float phi2)
{
    float deltaPhi = TMath::Abs(phi1-phi2);
    float deltaEta = eta1-eta2;
    if(deltaPhi > TMath::Pi())
        deltaPhi = TMath::TwoPi() - deltaPhi;
    return TMath::Sqrt(deltaEta*deltaEta + deltaPhi*deltaPhi);
}

bool isquark(int pdgid){
    if (abs(pdgid)==1) return true;
    if (abs(pdgid)==2) return true;
    if (abs(pdgid)==3) return true;
    if (abs(pdgid)==4) return true;
    if (abs(pdgid)==5) return true;
    if (abs(pdgid)==6) return true;
    if (abs(pdgid)==7) return true;
    if (abs(pdgid)==8) return true;
    if (abs(pdgid)==21) return true;
    return false;
}


int IsFromHadronicTop(int MotherMatchpdgid,int Matchpdgid,int GrandMotherMatchpdgid)
{
    int FromHadronicTop=0;
    if (abs(MotherMatchpdgid)==24 || abs(GrandMotherMatchpdgid)==24) FromHadronicTop=1;
    if (abs(MotherMatchpdgid)==6 || abs(GrandMotherMatchpdgid)==6) FromHadronicTop=1;
    return FromHadronicTop;
}



RVecI JetIsFromHadTop(Vec_t GenJet_eta, Vec_t GenJet_phi, Vec_t Jet_genJetIdx, Vec_t gen_eta, Vec_t gen_phi, Vec_t gen_pdgid, Vec_t gen_genPartIdxMother, Vec_t gen_status, float matchdR=0.3)
{
    RVecI Jet_isFromHadronicTop(Jet_genJetIdx.size());
	for (size_t i = 0; i < Jet_genJetIdx.size(); i++){
	    if (Jet_genJetIdx[i]==-1){
		continue;}
	    float dR=999.0;
	    int match=0;
	    float MatchedObject_eta=GenJet_eta[Jet_genJetIdx[i]];
	    float MatchedObject_phi=GenJet_phi[Jet_genJetIdx[i]];
	    int foundtop=0;
	    int foundW=0;
	    int foundb=0;
	    for (size_t j = 0; j < gen_eta.size(); j++){
		if(!isquark(abs(gen_pdgid[j]))) continue;
		float myDR=DeltaR(MatchedObject_eta,MatchedObject_phi,gen_eta[j],gen_phi[j]);
		if(myDR<0.3 && myDR<dR){
		    match=1;
		    int moindex=j;
		    for (int k=0;k<9;k++){
			int pdgid=gen_pdgid[moindex];
			cout<<"MatchID= "<<pdgid<<endl;
			if(abs(pdgid)==24) cout<<"Found W"<<endl;
			if(abs(pdgid)==5) cout<<"Found b"<<endl;
			if(abs(pdgid)==24){foundW=1;}
			if(abs(pdgid)==5){foundb=1;}
			if(abs(pdgid)==6 && abs(gen_pdgid[gen_genPartIdxMother[moindex]])!=6){
			    cout<<"Found top"<<endl;
			    foundtop=(1000+(100*foundW)+(10*foundb));
			    if(pdgid<0)foundtop=-1*(foundtop);
			    break;}
			moindex=gen_genPartIdxMother[moindex];
		    }		    
		    dR=myDR;}
		if (abs(foundtop)>0) break;
	    }
	    //if(abs(foundtop)==1000){
		//cout<<"foundtop= "<<foundtop<<endl;}
	    cout<<"---------------------------"<<endl;
	    Jet_isFromHadronicTop[i]=foundtop;
	}
	return Jet_isFromHadronicTop;
}

		
bool EventHasW(Vec_t pdgid)
{
    for (size_t i = 0; i < pdgid.size(); i++) {
	if (abs(pdgid[i])==24) return true;}
    return false;
}



RVecF Varbutindices(Vec_t var, Vec_t indices)
{
    
    RVecF Varfromindices(2);
    //Varfromindices[0]=1;
    //Varfromindices[0]=2;
    
    for (size_t i = 0; i < indices.size(); i++) {
        float ind=indices[i];
        if (var.size()>i) Varfromindices[i]=var[ind];
        else{ 
            Varfromindices[i]=-999; //Protection for if there is no value for var at i
            std::cout<<"Check issue in Varbutindices, size of variables not compatible"<<endl;
        }
    } 
    return Varfromindices;
}

/*
bool dr_cuts(Vec_t el_eta, Vec_t el_phi)
{
   auto el_dr = DeltaR(el_eta[0], el_eta[1], el_phi[0], el_phi[1]);
   if (el_dr < 0.4) {
      return false;}
   return true;
}
*/

int ChargeFlip_Category(float MyElectron_pt1,float MyElectron_pt2,float MyElectron_eta1,float MyElectron_eta2)
{
    int el1LMH,el2LMH,el1BE,el2BE;

    el1LMH=2;
    if (MyElectron_pt1<=25){el1LMH=1;}
    if (MyElectron_pt1>=50){el1LMH=3;}

    el2LMH=2;
    if (MyElectron_pt2<=25){el2LMH=1;}
    if (MyElectron_pt2>=50){el2LMH=3;}

    el1BE=1;
    if (abs(MyElectron_eta1)>=1.479){el1BE=2;}


    el2BE=1;
    if (abs(MyElectron_eta2)>=1.479){el2BE=2;}

    int cat=el1BE*1000 + el1LMH*100 + el2BE*10 + el2LMH;


    if (cat==1111) return 1;
    if (cat==1211 || cat==1112) return 2;
    if (cat==1212) return 3;
    if (cat==1311 || cat==1113) return 4;
    if (cat==1312 || cat==1213) return 5;
    if (cat==1313) return 6;
    if (cat==2121) return 7;
    if (cat==2221 || cat==2122) return 8;
    if (cat==2222) return 9;
    if (cat==2321|| cat==2123) return 10;
    if (cat==2322 || cat==2223) return 11;
    if (cat==2323) return 12;

    if (cat==1121 || cat==2111) return 13;
    if (cat==1221 || cat==2112) return 14;
    if (cat==2211 || cat==1122) return 15;
    if (cat==1222 || cat==2212) return 16;
    if (cat==1321 || cat==2113) return 17;
    if (cat==2311 || cat==1123) return 18;
    if (cat==1322 || cat==2213) return 19;
    if (cat==2312 || cat==1223) return 20;
    if (cat==1323 || cat==2313) return 21;

    return 22;
}


RVecF getMuonWeight(TString type,int nMuon,RVecF Muon_pt,RVecF Muon_eta){
    
    
    RVecF Weight(6);
    Double_t leptonWeight = 1.0, leptonWeightUp = 1.0, leptonWeightDown = 1.0;
    Double_t triggerWeight = 1.0, triggerWeightUp = 1.0, triggerWeightDown = 1.0;
    
    if(type=="mu"){

	TString muonIsoFileName="./config/weights/muon/Efficiencies_muon_generalTracks_Z_Run2016_UL_ISO.root";
	TString muonIsoHistName="NUM_LooseRelIso_DEN_LooseID_abseta_pt";
	TString muonIDFileName="./config/weights/muon/Efficiencies_muon_generalTracks_Z_Run2016_UL_ID.root";
	TString muonIDHistName="NUM_MediumID_DEN_TrackerMuons_abseta_pt";

	
	TFile* muonIsoFile = TFile::Open(muonIsoFileName,"READ");

	if (!muonIsoFile) std::cout << "Muon iso file not found!" << std::endl;
	auto _muonIsoSF = (TH2F*)muonIsoFile->Get(muonIsoHistName);//+"/pt_abseta_ratio");
	_muonIsoSF->SetDirectory(0);
	muonIsoFile->Close();

	TFile* muonIDFile = TFile::Open(muonIDFileName,"READ");
	if (!muonIDFile) std::cout << "Muon ID file not found!" << std::endl;
	auto _muonIDSF = (TH2F*)muonIDFile->Get(muonIDHistName);//+"/pt_abseta_ratio");
	_muonIDSF->SetDirectory(0);
	muonIDFile->Close();


	// TFile* muonTrigFile = TFile::Open(muonTrigFileName,"READ");
	// if (!muonTrigFile) std::cout << "Muon trig file not found!" << std::endl;
	// _muonTrigSF = (TH2F*)muonTrigFile->Get(muonTrigHistName+"/pt_abseta_ratio")->Clone();
	// _muonTrigSF->SetDirectory(0);
	// muonTrigFile->Close();

	// TFile* muonTkFile = TFile::Open(muonTkFileName,"READ");
	// if (!muonTkFile) std::cout << "Muon tracker file not found!" << std::endl;
	// _muonTkSF = (TGraphAsymmErrors*)muonTkFile->Get("ratio_eff_aeta_dr030e030_corr")->Clone();
	// //  _muonTkSF->SetDirectory(0);
	// muonTkFile->Close();
	for (int i=0;i<nMuon;i++){
	    //std::cout<<Muon_pt[i]<<endl;
	    //std::cout<<Muon_eta[i]<<endl;
	    
	    //Get the bin shared by iso and id SFs
	    //Int_t xAxisBin = _muonIsoSF->GetXaxis()->FindBin(float(Muon_pt[i]));
	    //_muonIsoSF->Dump();
	    
	    Int_t xAxisBin=_muonIsoSF->GetXaxis()->FindBin(Muon_pt[0]);
	    
	    if (Muon_pt[i] > 120.) xAxisBin = _muonIsoSF->GetXaxis()->FindBin(119.);
	    
	    Int_t yAxisBin = _muonIsoSF->GetYaxis()->FindBin(std::fabs(Muon_eta[i]));
	    if (std::fabs(Muon_eta[i]) > 2.4) yAxisBin = _muonIsoSF->GetYaxis()->FindBin(2.39);
	    
	    //And now get the iso and id SFs/uncs
	    Float_t isoSF = _muonIsoSF->GetBinContent(xAxisBin,yAxisBin);
	    Float_t isoUnc = _muonIsoSF->GetBinError(xAxisBin,yAxisBin);
	    Float_t idSF = _muonIDSF->GetBinContent(xAxisBin,yAxisBin);
	    Float_t idUnc = _muonIDSF->GetBinError(xAxisBin,yAxisBin);
	    
	    // //Get the bin for trigger SF
	    // Int_t xAxisBinTrig = _muonTrigSF->GetXaxis()->FindBin(Muon_pt[i]);
	    // if (Muon_pt[i] > 500.) xAxisBinTrig = _muonTrigSF->GetXaxis()->FindBin(499.);
	    // Int_t yAxisBinTrig = _muonTrigSF->GetYaxis()->FindBin(std::fabs(Muon_eta[i]));
	    // if (std::fabs(Muon_eta[i]) > 2.4) yAxisBinTrig = _muonTrigSF->GetYaxis()->FindBin(2.39);
	    // //Get the trigSF
	    // Float_t trigSF = _muonTrigSF->GetBinContent(xAxisBinTrig,yAxisBinTrig);
	    // Float_t trigUnc = _muonTrigSF->GetBinError(xAxisBinTrig,yAxisBinTrig);
	    
	    // //Evaluate muon tk
	    Float_t tkSF = 1;//_muonTkSF->Eval(std::fabs(Muon_eta[i]));
	    
	    leptonWeight *= isoSF * idSF * tkSF;
	    leptonWeightUp *= (isoSF + isoUnc) * (idSF + idUnc) * tkSF;
	    leptonWeightDown *= (isoSF - isoUnc) * (idSF - idUnc) * tkSF;
	    
	    // triggerWeight = trigSF;
	    // triggerWeightUp = trigSF + trigUnc;
	    // triggerWeightDown = trigSF - trigUnc;


	}
	Weight[0]=leptonWeight;
	Weight[1]=leptonWeightUp;
	Weight[2]=leptonWeightDown;
	Weight[3]=0;//triggerWeight;
	Weight[4]=0;//triggerWeightUp;
	Weight[5]=0;//triggerWeightDown;
    
    }
    else{
	Weight[0]=0;
	Weight[1]=0;
	Weight[2]=0;
	Weight[3]=0;
	Weight[4]=0;
	Weight[5]=0;
    }
return Weight;
}
