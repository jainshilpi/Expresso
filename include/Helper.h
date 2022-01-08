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