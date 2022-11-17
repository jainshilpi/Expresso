chmod +x plot+.py
chmod +x expresso.py
pip install -e .
chmod +x modules/createJSON.py

alias createJSON="python modules/createJSON.py"

ehelp () {
    python expresso.py --help
}


phelp () {
    python plot+.py --help
}

ana () {
    ls Analysis/
}

