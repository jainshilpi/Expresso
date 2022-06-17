#!/usr/bin/env bash
source /afs/cern.ch/user/a/akapoor/.bashrc
cd /afs/cern.ch/user/a/akapoor/workspace/HEP2022/Expresso
source /cvmfs/sft.cern.ch/lcg/views/dev3cuda/latest/x86_64-centos7-gcc8-opt/setup.sh

echo "Here in wrap"
pip install -e .
echo "Running command:" $@
timeout 4h $@ || exit $?
