unset PYTHONPATH
conda create --name my-coffea python=3.9 pip
conda activate my-coffea
pip install coffea pyyaml
conda install -c conda-forge xrootd ndcctools dill conda-pack
conda activate my-coffea
