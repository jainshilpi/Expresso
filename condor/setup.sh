#!/bin/sh

source /cvmfs/cms.cern.ch/cmsset_default.sh
export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git.daily
ulimit -s unlimited
source /cvmfs/sft.cern.ch/lcg/views/LCG_98py3cu10/x86_64-centos7-gcc8-opt/setup.sh
echo "Running"
echo "${@}"
echo ${@}
eval ${@}
