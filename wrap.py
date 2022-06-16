#!/usr/bin/env bash
source /afs/cern.ch/user/a/akapoor/.bashrc
cd /afs/cern.ch/user/a/akapoor/workspace/HEP2022/Expresso
conda activate my-coffea-env
#tar -zxf my-coffea-env.tar.gz
#source coffeaenv/bin/activate
echo "Here in wrap"
pip install -e .
echo "Running command:" $@
timeout 4h $@ || exit $?
