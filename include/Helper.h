#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
 
using namespace ROOT;
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;

using Vec_t = const ROOT::RVec<float>&;
using RVecF = RVec<float>;
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