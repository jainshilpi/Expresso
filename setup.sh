chmod +x plot+.py
chmod +x expresso.py
pip install -e .

ehelp () {
    python expresso.py --help
}


phelp () {
    python plot+.py --help
}

ana () {
    ls Analysis/
}

