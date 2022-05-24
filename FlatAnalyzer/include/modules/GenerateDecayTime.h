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
