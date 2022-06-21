#!/usr/bin/env bash
source "/publicfs/cms/user/kapoor/miniconda3/etc/profile.d/conda.sh"
cd /publicfs/cms/user/kapoor/2022/Expresso
conda activate mycoffea
echo "Here in wrap"
pip install -e .
touch done.txt
echo "Running command:" $@
timeout 4h $@ || exit $?
