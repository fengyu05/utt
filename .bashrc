# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"


# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
xterm-color) color_prompt=yes;;
esac


# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
fi


# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
. /etc/bash_completion
fi

##########################################################################################
# gnefihz begin here
##########################################################################################
if [ -d ~/bin ]; then
  PATH=$PATH:~/bin
fi
if [ -d ~/utt ]; then
  PATH=$PATH:~/utt
fi

export EDITOR='vi'
export localhost=127.0.0.1
export HOME_IP=172.21.106.42
export PLAY=$HOME/workspace/playground
export HOST_NAME=`cat $HOME/.HOST_NAME`
export WP=$HOME/workspace

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias cls="clear"
alias more="less" # more is less
alias listjar="jar tf"
alias check_port='netstat -lpn'
alias blaze='ligradle'
alias svn='svin'
alias rf='record_file'
alias list='list_file'
alias lf='load_file'
alias hfs="hadoop fs"
alias wp='cd ~/workspace'
alias forecast_wp='wp;cd forecast_trunk'
alias network_wp='wp;cd network_trunk'
alias mlutt='wp;cd mlutt'
alias adsutt='wp;cd adsutt'
alias adsrele='wp;cd ads-relevance_trunk'
alias tscp='wp;cd tscp_trunk'
alias cd_liar='network_wp; cd liar/'
alias cd_lame='network_wp; cd liar/lame/java/com/linkedin/liar/lame/'
alias cd_liarloser='network_wp; cd liar/loser/java/com/linkedin/liar/'
alias cd_loser='wp; cd loser_trunk'
alias cd_csp_impl='network_wp; cd sasbe/cspserving-impl'
alias cd_network='network_wp;'
alias cd_recls='wp;cd recls'
alias cd_model_sample='recls; cd autobahn/models/lame'
alias recls='wp;cd recls'
alias cd_pg='wp;cd playground'
alias uscp='wp;cd uscp_trunk'
alias ssh_prod_csp='ssh-range -f PROD-ELA4 csp-service'
alias gitcommit='git commit -m whatever'

alias rf1='record_file $F1'
alias rf2='record_file $F2'
alias rf3='record_file $F3'
alias rf4='record_file $F4'
alias rf5='record_file $F5'
alias rf6='record_file $F6'
alias rf7='record_file $F7'
alias rf8='record_file $F8'
alias rf9='record_file $F9'

PS1="=== $HOST_NAME === \u@\w\$"

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
PS1="\[\e]0;\u@\h: \w\a\]$PS1"
;;
*)
;;
esac

sure () {
# call with a prompt string or use a default
read -r -p "${1:-Are you sure? [y/N]} " response
case $response in
[yY][eE][sS]|[yY])
return 0
;;
*)
return 1
;;
esac
}

non_empty () {
if [ $# -eq 0 ]; then
echo "usage: cmd arg1"
return 1
fi
return 0
}

function rebash() {
source ~/.bashrc
}

function bashrc() {
vim ~/.bashrc
cp ~/.bashrc ~/utt/.bashrc
}

function vimrc() {
vim ~/.vimrc
cp ~/.vimrc ~/vimrc
}

function pg() {
  cd ~/playground/network_trunk
}

gnefihz_config_file=(.bashrc .vimrc .vim motto)
function upload_config() {
sure 'Are you sure upload config to /home/gnefihz?'
if [ $? -eq 0 ]; then
echo 'uploading...'
gnefihz_home=/home/gnefihz
for item in ${gnefihz_config_file[*]}
do
cp -r ~/$item $gnefihz_home
done
else
echo 'cancel'
fi
}

function download_config() {
sure 'Are you sure download config file from /home/gnefihz to local?'
if [ $? -eq 1 ]; then
return
fi
sure 'Are you sure again?'
if [ $? -eq 0 ]; then
echo 'downloading ....'
gnefihz_home=/home/gnefihz
for item in ${gnefihz_config_file[*]}
do
cp -r $gnefihz_home/$item ~/
done
else
echo 'cancel'
fi
}


function listfile() {
LFS=`find . -name $1`
LFA=( $LFS)
LF=${LFA[0]}

echo "All"
echo $LFS
echo "Selected"
echo $LF
}

function ggg() {
  if [ $# -lt 1 ] ; then
    echo "usage: greplg keyword"
    return
  fi
  source_file $WP | xargs -I "fn" grep "$1" -n -B 2 --with-filename -A 2 --color=auto "fn"
}

function gg() {
if [ $# -lt 1 ] ; then
echo "usage: greplg keyword"
return
fi
source_file | xargs -I "fn" grep "$1" -n -B 2 --with-filename -A 2 --color=auto "fn"
}

function gglist() {
if [ $# -lt 1 ] ; then
echo "usage: greplg keyword"
return
fi
source_file | xargs -I "fn" grep "$1" --with-filename "fn" | cut -d: -f 1 | uniq
}

function ggeditall() {
if [ $# -lt 1 ] ; then
echo "usage: greplg keyword"
return
fi
F=`source_file | xargs -I "fn" grep "$1" --with-filename "fn" | cut -d: -f 1 | uniq`
vim $F
}

function text_file() {
  find . -name "*.java" -o -name "*.js" -o -name "*.html" -o -name "*.pig" \
      -o -name "*.jobs" -o -name "*.py" -o -name "*.properties"
}

function source_file() {
  if [ $# -lt 1 ] ; then
    TARGET=.
  else
    TARGET=$1
  fi
  find $TARGET -type d \( -path "*/.svn" -o -path "*/build" -o -path "*/.git" \) -prune -o -type f -exec grep -Il . {} \;
}

_mapff() {
i=1
for file in $* 
do
  export F$i=$file
  echo "[F$i]" $file 
  let " i+= 1"
done
}

_ff() {
  if [ $# -lt 1 ] ; then
    echo "usage: ff filepattern"
    return
  fi
  find . -name *"$1"* -o -type d \( -path "*/build" -o -path "*/.svn" -o -path "*/.git" \) -prune | egrep -v "./build|.git|.svn"
}

ff() {
if [ $# -lt 1 ] ; then
echo "usage: ff filepattern"
return
fi
_mapff `find . -name *"$1"* -o -type d \( -path "*/build" -o -path "*/.svn" -o -path "*/.git" \) -prune | egrep -v "./build|.git|.svn"`
}

gff() {
if [ $# -lt 1 ] ; then
echo "usage: ff filepattern"
return
fi
_mapff `find $WP -name *"$1"* -o -type d \( -path "*/build" -o -path "*/.svn" -o -path "*/.git" \) -prune | egrep -v "./build|.git|.svn" | grep --color $1`
}

load_file() {
if [ $# -lt 1 ] ; then
echo ""
else
vim -c ":qa" $1
fi
}

editall () {
vim $F1 $F2 $F3 $F4 $F5 $F6 $F7 $F8 $F9
}

loadall () {
rf $F1; rf $F2; rf $F3;rf $F4;rf $F5;rf $F6;rf $F7;rf $F8;rf $F9;
}

function motto() {
sort -R ~/motto | head -n 1
}

function build_forecast() {
  ligradle build
  ff *.zip
  cp $F1 ~/tmp/
  cp $F3 ~/tmp/
  cp $F3 ~/tmp/
}

function magic() {
  ssh -K eat1-magicgw01.grid.linkedin.com
}

function copy_from_magic() {
  if [ $# -lt 1 ] ; then
    echo "copy_from_magic path"
    return 1
  fi
  name=`basename $1`
  echo "ssh copying..."
  ssh -q -K -tt eat1-magicgw01.grid.linkedin.com "rm -rf ~/.magic_file_cache;mkdir ~/.magic_file_cache;hadoop fs -copyToLocal $1 ~/.magic_file_cache/;copy_to_home ~/.magic_file_cache/$name" 
  mv ~/incoming/$name ./$name
}

function canasta() {
  ssh -K eat1-hcl0041.grid.linkedin.com
}

function kill_sth() {
kill `ps aux | grep $1 | grep -v grep | cut -d " " -f 4`
}

function copy_to_magic() {
  scp -r $1 zhdeng@eat1-magicgw01.grid.linkedin.com:~/incoming
}

function copy_to_canasta() {
  scp -r $1 zhdeng@eat1-hcl0041.grid.linkedin.com:~/incoming
}

function copy_to_home() {
  scp -r $1 zhdeng@$HOME_IP:~/incoming
}

function copy_to_laptop() {
  scp -r $1 zhdeng@zhdeng-mn1:~/incoming
}


function record_file() {
  if [ $# -lt 1 ] ; then echo "Need one arg"; fi
  touch ./.filelist
  echo $1 >> ./.filelist 
  cp ./.filelist ./.bak_filelist
  tail -20 ./.bak_filelist > ./.filelist 
  lf $1
}

function list_file() {
  _mapff `tac ./.filelist`
}

function svn_update_review() {
  svn review --update $1 --changelist $2
}

function svn_review_changelist() {
  svn review --changelist $1
}

function svn_remove_cl() {
  svn status |\
    sed -n "/--- Changelist '$1':/,/--- Changelist.*/p" |\
    grep -v '^--- Changelist' |\
    awk '{print $2}' |\
    xargs svn changelist --remove
}

function gradle_clean_build_zip() {
  find . -name "*.zip" | xargs -Ifn rm fn
}

function deploy_csp_withconfig() {
  mint dev build build-cfg deploy -w sasbe-cspserving-war -f QEI2
}

function cut_two_edge() {
  cat $1 | cut -c $2- | rev | cut -c $3- | rev
}

function deploy_csp() {
  mint deploy --config QEI2 -w sasbe-cspserving-war
}

function config_csp() {
  mint build-cfg QEI2 -w sasbe-cspserving-war
}

function vld_scin_model() {
  ~/voldemort/bin/voldemort-shell.sh ScinModelCoefficientsV2 tcp://ei-voldemort-read-only-vip.stg.linkedin.com:10103/
}

function vld_single_node() {
  cd $HOME/voldermort
  bin/voldemort-server.sh config/single_node_cluster /tmp/voldemort.log &
}

function vld_test_client() {
  ~/voldermort/bin/voldemort-shell.sh test tcp://localhost:6666
}

############### sample section
function _for_item() {
array=(one two three four [5]=five)
for item in ${array[*]}
do
printf " %s\n" $item
done
}


function _for_loop() {
for i in {1..1000}
do
echo "gnefihz$i@google.com"
done
}
# User specific aliases and functions
