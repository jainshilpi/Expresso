#!/bin/bash


source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc8-opt/setup.sh
pip install git+https://github.com/cms-nanoAOD/correctionlib.git@master
#pip install correctionlib

ReadInfocsv (){
    echo "TotalEvents"
    cat $1 | cut -d ',' -f5 | jq -s add
    echo "EventsPassed"
    cat $1 | cut -d ',' -f4 | jq -s add
    echo "TotalFiles"
    cat $1 | cut -d ',' -f3 | jq -s length
}

nbc (){
    jupyter nbconvert --to script $1
}



getremoteskimcommand(){
    sname="$1"
    outfolder="$2"
    remotefilelist="$3"
    analysis="$4"
    maindir=$PWD

    echo "Run the command below in terminal (as one command) to Skim $1 sample remotely! Output skims will be stored in $2. List of remote files will be taken from $3"
    echo "-----------------------------------"
    echo "maindir=$PWD;cd condor; a=0; while read -r line; do echo \$a; condor_submit job.sh -append \"arguments = cd $maindir && python Skimmer.py --name $sname --file root://xrootd-cms.infn.it//\${line} --saveroot --outfolder $outfolder --analysis $analysis --saveroot --outsuffix $sname-\$a --multithreaded --xsec 1 --istype mc \"; let \"a += 1\"; done <$remotefilelist; cd .."
    echo "-----------------------------------"
}
