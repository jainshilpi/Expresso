echo "########### Setting up env for expresso ##############"

system=$(uname --all)
if [[ "$system" == *"WSL2"* ]]; then
   echo "In wsl2"
   conda activate py37_coffea_hep
elif [[ "$system" == *"lxslc"* ]]; then
   conda activate expresso
elif [[ "$system" == *"lxplus"* ]]; then
    conda activate expresso
else
    echo "Are you in supported node?"
fi
   
      

chmod +x plot+.py
chmod +x expresso.py
pip install -e .
chmod +x modules/createJSON.py


ehelp () {
    python expresso.py --help
}


phelp () {
    python plot+.py --help
}

ana () {
    ls Analysis/
}

