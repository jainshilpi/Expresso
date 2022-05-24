#!/bin/sh
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
alias home='cd /afs/cern.ch/user/a/akapoor'
alias work='cd /afs/cern.ch/work/a/akapoor'
alias cq='condor_q'
alias iget='wget --certificate=/afs/cern.ch/user/a/akapoor/.globus/usercert.pem --private-key=/afs/cern.ch/user/a/akapoor/.globus/userkey.pem'


source /cvmfs/cms.cern.ch/cmsset_default.sh
export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git.daily


#cernbox eos
export EOS_MGM_URL=root://eosuser.cern.ch
#export X509_USER_PROXY=/tmp/x509up_u72490
export X509_USER_PROXY=/afs/cern.ch/user/a/akapoor/proxy/myx509
alias cernboxhome='cd /eos/user/a/akapoor'
export cernboxdir=/eos/user/a/akapoor
alias webhome='cd /eos/user/a/akapoor/www/Webfolder'

#export PS1='\e[0;1m\e[42m\h \e[m\e[0;1m\e[43m \W \e[m$'
#export PS1='\[\e[0;1m\]\[\e[42m\]\h\[\e[m\]\[\e[0;1m\]\[\e[101m\]\W\[\e[m\]$'
export PS1="\[\e[0;32m\]\h:\w\$ \[\e[0m\]"
#export LC_CTYPE=en_US.UTF-8
#code () { VSCODE_CWD="$PWD" open -n -b "com.microsoft.VSCode" --args $* ;}

extract () {
   if [ -f $1 ] ; then
       case $1 in
           *.tar.bz2)   tar xvjf $1;;
           *.tar.gz)    tar xvzf $1;;
           *.bz2)       bunzip2 $1 ;;
           *.rar)       unrar x $1 ;;
           *.gz)        gunzip $1  ;;
           *.tar)       tar xvf $1 ;;
           *.tbz2)      tar xvjf $1;;
           *.tgz)       tar xvzf $1;;
           *.zip)       unzip $1   ;;
           *.Z)         uncompress $1  ;;
           *.7z)        7z x $1;;
           *) echo "don't know how to extract '$1'..." ;;
       esac
   else
       echo "'$1' is not a valid file!"
   fi
}

alias q='exit'
alias t='time'

sbs() { du -b --max-depth 1 | sort -nr | perl -pe 's{([0-9]+)}{sprintf "%.1f%s", $1>=2**30? ($1/2**30, "G"):    $1>=2**20? ($1/2**20, "M"): $1>=2**10? ($1/2**10, "K"): ($1, "")}e';}

ulimit -s unlimited

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/eos/cms/store/group/phys_egamma/akapoor/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/eos/cms/store/group/phys_egamma/akapoor/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/eos/cms/store/group/phys_egamma/akapoor/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/eos/cms/store/group/phys_egamma/akapoor/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

