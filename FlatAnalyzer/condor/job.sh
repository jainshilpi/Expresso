universe = vanilla
+JobFlavour = "workday"
executable = setup.sh
#arguments = "Trainer_cmsml_exp_with3rdnodecut.py Configs/PFElectronID/PFElectronConfig_lowpT_12_2_allnewsamples_3rdnodecut"
log = test.log
output = condor_output/outfile.$(Cluster).$(Process).out
error = condor_output/errors.$(Cluster).$(Process).err
#request_GPUs = 1
#request_CPUs = 4
#getenv = True
x509userproxy = $ENV(X509_USER_PROXY)
use_x509userproxy = True
RequestCpus = 4
RequestMemory = 2048
stream_output = True
#notify_user = akapoor@cern.ch
#+testJob = True
queue 
