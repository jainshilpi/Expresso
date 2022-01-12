#!/bin/sh

sname="$1"
outfolder="$2"
remotefilelist="$3"

echo "Run the command below in terminal (as one command) to Skim $1 sample remotely! Output skims will be stored in $2. List of remote files will be taken from $3"
echo "-----------------------------------"
echo "maindir=$PWD;cd condor; a=0; while read -r line; do echo \$a; condor_submit job.sh -append \"arguments = cd $maindir && python Skimmer.py --name $sname --file root://xrootd-cms.infn.it//\${line} --saveroot --outfolder $outfolder --outsuffix $sname-\$a\"; let \"a += 1\"; done <$remotefilelist; cd .."
echo "-----------------------------------"
