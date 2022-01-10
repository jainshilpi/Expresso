using Vec_t = const ROOT::RVec<float>&;
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
    el1LMH=1*(MyElectron_pt1<25) + 2*(MyElectron_pt1>=25 && MyElectron_pt1<50) + 3*(MyElectron_pt1>=50);
    el2LMH=1*(MyElectron_pt2<25) + 2*(MyElectron_pt2>=25 && MyElectron_pt2<50) + 3*(MyElectron_pt2>=50);
    
    el1BE=1*(abs(MyElectron_eta1)<1.479) + 2*(abs(MyElectron_eta1)>=1.479);
    el2BE=1*(abs(MyElectron_eta2)<1.479) + 2*(abs(MyElectron_eta2)>=1.479);
    
    
    if (el1BE==1 && el1LMH==1 && el2BE==1 && el2LMH==1)
        return 0;
    if (el1BE==1 && el1LMH==2 && el2BE==1 && el2LMH==1)
        return 1;
    if (el1BE==1 && el1LMH==2 && el2BE==1 && el2LMH==2)
        return 2;
    if (el1BE==1 && el1LMH==3 && el2BE==1 && el2LMH==1)
        return 3;
    if (el1BE==1 && el1LMH==3 && el2BE==1 && el2LMH==2)
        return 4;
    if (el1BE==1 && el1LMH==3 && el2BE==1 && el2LMH==3)
        return 5;
    if (el1BE==2 && el1LMH==1 && el2BE==2 && el2LMH==1)
        return 6;
    if (el1BE==2 && el1LMH==2 && el2BE==2 && el2LMH==1)
        return 7;
    if (el1BE==2 && el1LMH==2 && el2BE==2 && el2LMH==2)
        return 8;
    if (el1BE==2 && el1LMH==3 && el2BE==2 && el2LMH==1)
        return 9;
    if (el1BE==2 && el1LMH==3 && el2BE==2 && el2LMH==2)
        return 10;
    if (el1BE==2 && el1LMH==3 && el2BE==2 && el2LMH==3)
        return 11;
    if (el1BE==1 && el1LMH==1 && el2BE==2 && el2LMH==1)
        return 12;
    if (el1BE==1 && el1LMH==2 && el2BE==2 && el2LMH==1)
        return 13;
    if (el1BE==2 && el1LMH==2 && el2BE==2 && el2LMH==1)
        return 14;
    if (el1BE==1 && el1LMH==2 && el2BE==2 && el2LMH==2)
        return 15;
    if (el1BE==1 && el1LMH==3 && el2BE==2 && el2LMH==1)
        return 16;
    if (el1BE==2 && el1LMH==3 && el2BE==1 && el2LMH==1)
        return 17;
    if (el1BE==1 && el1LMH==3 && el2BE==2 && el2LMH==2)
        return 18;
    if (el1BE==2 && el1LMH==3 && el2BE==1 && el2LMH==2)
        return 19;
    if (el1BE==1 && el1LMH==3 && el2BE==2 && el2LMH==3)
        return 20;
    return 21;
}