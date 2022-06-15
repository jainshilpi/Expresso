unset PYTHONPATH
conda create --name my-coffea-env python=3.9
conda activate my-coffea-env
conda install -c conda-forge coffea xrootd ndcctools dill conda-pack
conda activate my-coffea-env
