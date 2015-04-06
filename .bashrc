#.bashrc

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

export NETREPO=svn+ssh://svn.corp.linkedin.com/netrepo/network
export LIREPO=svn+ssh://svn.corp.linkedin.com/lirepo
export VENREPO=svn+ssh://svn.corp.linkedin.com/vendor

#export JAVA_HOME=/export/apps/jdk/JDK-1_6_0_27
#export JDK_HOME=/export/apps/jdk/JDK-1_6_0_27
export JAVA_HOME=/export/apps/jdk/JDK-1_8_0_5
export JDK_HOME=/export/apps/jdk/JDK-1_8_0_5
export NLS_LANG=American_America.UTF8

export M2_HOME=/local/maven

##########################################################################################
# zhdeng begin here
##########################################################################################
# append path
export ALL_NEW_PATH="
  $HOME/bin
  $HOME/bin/activator/activator-1.2.12
  $HOME/utt
  $HOME/adsutt
  $HOME/mlutt
  $HOME/spark/bin
  $HOME/expect
  /usr/local/apache-maven/bin
  $HOME/voldemort/bin
  /opt/likewise/bin
  $M2_HOME/bin
  $HOME/.rbenv/bin
  $JAVA_HOME/bin
  /usr/local/bin
  /usr/local/mysql/bin
  /usr/local/linkedin/bin
  /home/zhdeng/.linuxbrew/bin
  "

for newPath in $ALL_NEW_PATH
do
  if [ -d $newPath ]; then
    PATH=$PATH:$newPath
  fi
done


eval "$(rbenv init -)"

eval `keychain --eval --agents ssh github_rsa`
if [ -x /usr/bin/keychain ] ; then
	MYNAME=`/usr/bin/whoami`
	if [ -f ~/.ssh/${MYNAME}_at_linkedin.com_dsa_key ] ; then
	      /usr/bin/keychain ~/.ssh/${MYNAME}_at_linkedin.com_dsa_key
      	      . ~/.keychain/`hostname`-sh
	fi
fi

export EDITOR='vi'
export localhost=127.0.0.1
export HOME_IP=`ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'`
export HOST_NAME=`cat $HOME/.HOST_NAME`
export WP=$HOME/workspace
export M2_HOME=/usr/local/apache-maven
export M2=$M2_HOME/bin
export TSCPBE=$HOME/workspace/tscp-backend_trunk
export BAM_OFFLINE=$WP/recls/bam_offline

# ALIAS ALIAS
alias work='ssh zhdeng@zhdeng-ld1'
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias cls="clear"
alias more="less" # more is less
alias listjar="ls *.jar | xargs -Ifn sh -c 'echo fn;jar tf fn'"
alias check_port='netstat -lpn'
alias blaze='ligradle'
alias svn='svin'
alias gradle='ligradle'
alias rf='record_file'
alias list='list_file'
alias lf='load_file'
alias hfs="hadoop fs"
alias wp='cd ~/workspace'
alias forecast_wp='wp;cd forecast_trunk'
alias fcst_dep='ligradle offline:forecasting-offline-common:dependencies | tee dep.list'
alias network_wp='wp;cd network_trunk'
alias cd_mlutt='cd $HOME/mlutt'
alias cd_admm='cd $HOME/ars-admm_trunk'
alias cd_adsutt='cd $HOME/adsutt'
alias cd_adsrel='wp;cd ads-relevance_trunk'
alias cd_tscp='wp;cd tscp_trunk'
alias cd_tscpbe='wp;cd tscp-backend_trunk'
alias cd_ucf='wp;cd ucf_trunk'
alias cd_bam='wp;cd bam_trunk'
alias cd_bam_offline='wp;cd recls; cd bam-offline'
alias cd_bam_ev='wp;cd evaluator;'
alias cd_autoapprove='wp;cd autoadapprovalmlmodel;'
alias cd_metronome='wp;cd metronome_trunk'
alias cd_liar='network_wp; cd liar/'
alias cd_lame='network_wp; cd liar/lame/java/com/linkedin/liar/lame/'
alias cd_az='wp; cd azkaban'
alias cd_pig='wp; cd pig'
alias cd_avro='wp; cd avro'
alias cd_liarloser='network_wp; cd liar/loser/java/com/linkedin/liar/'
alias cd_loser='wp; cd loser_trunk'
alias cd_csp_impl='network_wp; cd sasbe/cspserving-impl'
alias cd_sasbe='network_wp; cd sasbe'
alias cd_network='network_wp;'
alias cd_recls='wp;cd recls'
alias cd_log='cd /export/content/lid/apps/apps/dev-i001/logs'
alias cd_tomcat_log='cd /export/content/lid/apps/tomcat/dev-i001/logs'
alias cd_fcst_log='cd /export/content/lid/apps/forecasting-service/dev-i001/logs' 
alias cd_fcst_war='cd $HOME/local-repo/com/linkedin/forecast/forecasting-service-war' 
alias tail_log='cd_log;tail -f apps.out'
alias fcst_monitoring='wp;cd fcst-monitoring'
alias tail_fcst_log='cd_fcst_log;tail -f forecasting-service.out' 
alias tail_tomcat_log='cd_tomcat_log;tail -f catalina.out'
alias cd_pg='wp;cd playground'
alias cd_insight='wp;cd insight'
alias cd_uscp='wp;cd uscp_trunk'
alias ssh_prod_csp='ssh-range -f PROD-ELA4 csp-service'
alias ssh_ei_csp='ssh-range -f EI1 csp-service'
alias gitcommit='git commit -m "by auto commiter"'
alias git_push_origin='git push -u origin master'
alias git_list_unpushed='git log origin/master..HEAD --name-only'
alias git_list_unpushed2='_mapff `git_list_unpushed | tail -n +6`'
alias kill_fg='kill -9 $(jobs -p)'
alias restli_get='curli --pretty-print "%s" -X GET -g'
alias build_and_release='ligradle build -x test;mint release'
alias git_info='git remote show origin'
alias build_without_test='ligrade build -x test'
alias jar_list='jar tf '
alias mint_devdeploy='mint build;mint release;mint build-cfg -f dev;mint release-cfg;mint deploy'
alias mint_qeideploy='mint build;mint release;mint build-cfg -f QEI1;mint release-cfg;mint deploy'
alias mint_qei2deploy='mint build;mint release;mint build-cfg -f QEI2;mint release-cfg;mint deploy'
alias undeploy_sas='mint undeploy -f QEI1 -w sas-war && mint kill && mint clean-containers'
alias deploy_sas='ligradle :sas:sas-war:build && mint build-cfg -f QEI1 -w sas-war && mint deploy -f QEI1 -w sas-war --debug-app'
alias deploy_sas2='ligradle :sas:sas-war:build && mint build-cfg -f QEI2 -w sas-war && mint deploy -f QEI2 -w sas-war --debug-app'
alias deploy_zookeeper='mint deploy -w zookeeper-war'
alias aws_dev='ssh -i ~/.keycache/amazon.pem ec2-user@54.187.146.185'
alias fcst_do='_user_do fcst'
alias bids_do='_user_do bids'
alias liads_do='_user_do liads'
alias fcst_init='_user_do fcst kinit -kt fcst.headless.keytab fcst'
alias bids_init='_user_do bids kinit -kt bids.headless.keytab bids'
alias liads_init='_user_do liads kinit -kt liads.headless.keytab liads'
alias sibyl='cd ~/pip_dist/sibyl'
alias tscpbe='./tscebe'
alias pip_upload='python setup.py sdist bdist_wheel upload'
alias tscp_deploy_all_fcst='./tscpbe deploy scin & ./tscpbe deploy inmail & ./tscpbe deploy pacing & ./tscpbe deploy bids'

alias rf1='record_file $F1'
alias rf2='record_file $F2'
alias rf3='record_file $F3'
alias rf4='record_file $F4'
alias rf5='record_file $F5'
alias rf6='record_file $F6'
alias rf7='record_file $F7'
alias rf8='record_file $F8'
alias rf9='record_file $F9'

bind '"\eOP":"vim $F1\n"'
bind '"\eOQ":"vim $F2\n"'
bind '"\eOR":"vim $F3\n"'
bind '"\eOS":"vim $F4\n"'
bind '"\e[15~":"vim $F5\n"'
bind '"\e[17~":"vim $F6\n"'
bind '"\e[18~":"vim $F7\n"'
bind '"\e[19~":"vim $F8\n"'
bind '"\e[20~":"vim $F9\n"'
bind '"\e[21~":"vim $F10\n"'

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
  find $TARGET -type d \( -path "*/.svn" -o -path "*/build" -o -path "*/.git"  \) -prune -o \
  -type f \( -iname "tags" \) -prune -o -type f -exec grep -Il . {} \;
}

function list_all_build() {
  _mapff `find . -name 'build.gradle'`
}

_mapff() {
i=1
export __all_ff=$* 
for file in $* 
do
  if ((i % 2 == 0))
  then
    printf "\e[1;32m"
  fi
  export F$i=$file
  echo "[F$i]" $file 
  let " i+= 1"
  printf "\e[0m"
done
}

_ff() {
  if [ $# -lt 1 ] ; then
    echo "usage: ff filepattern"
    return
  fi
# \* escaping the asterisk avoid shell expanding
  find . -name \*"$1"\* -o -type d \( -path "*/build" -o -path "*/.svn" -o -path "*/zip" -o -path "*/.git" \) -prune | egrep -v "./build|.git|.svn|./zip"
}

_ffb() {
  if [ $# -lt 1 ] ; then
    echo "usage: ff filepattern"
    return
  fi
  find . -name \*"$1"\* -o -type d \( -path "*/.svn" -o -path "*/.git" \) -prune | egrep -v ".git|.svn"
}

ff() {
  _mapff `_ff $*`
}

ffb() {
  _mapff `_ffb $*`
}

gff() {
if [ $# -lt 1 ] ; then
echo "usage: ff filepattern"
return
fi
_mapff `find $WP -name \*"$1"\* -o -type d \( -path "*/build" -o -p "*/zip" -o -path "*/.svn" -o -path "*/.git" \) -prune | egrep -v "./build|.git|.svn|./zip" | grep --color $1`
}

load_file() {
if [ $# -lt 1 ] ; then
echo ""
else
vim -c ":qa" $1
fi
}

editall () {
vim $__all_ff 
}

loadall () {
rf $F1; rf $F2; rf $F3;rf $F4;rf $F5;rf $F6;rf $F7;rf $F8;rf $F9;
}

function motto() {
sort -R ~/motto | head -n 1
}

function magic() {
  ssh -K eat1-magicgw01.grid.linkedin.com
}

function nertz() {
  ssh -K eat1-nertzgw01.grid.linkedin.com
}

function nertz2() {
  ssh -K eat1-nertzgw02.grid.linkedin.com
}

function canasta() {
  ssh -K eat1-hcl0041.grid.linkedin.com
}

function kill_sth() {
kill `ps aux | grep $1 | grep -v grep | cut -d " " -f 4`
}


function prun() {
  echo $*
  eval "$*"
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
  if [ $# -lt 2 ]; then
    echo "svn_update_review reviewNo changelist"
    return 1
  fi
  svn review --update $1 --changelist $2
}

function svn_changelist_add() {
  if [ $# -lt 2 ]; then
    echo "svn_changelist_add changelist file"
    return 1
  fi
  svn changelist $1 $2
}

function svn_review_changelist() {
  svn review --changelist $1
}

function svn_remove_cl() {
  svn status | sed -n "/--- Changelist '$1':/,/--- Changelist.*/p" | grep -v '^--- Changelist' | cut -c 2- | \
    xargs svn changelist --remove
}

function gradle_clean_build_zip() {
  find . -name "*.zip" | xargs -Ifn rm fn
}

function deploy_csp_withconfig() {
  mint dev build build-cfg deploy -w sasbe-cspserving-war -f QEI1 
}

function deploy_campaign_withconfig() {
  echo "mint dev build build-cfg deploy -w sasbe-campaign-war -f QEI1"
  mint dev build build-cfg deploy -w sasbe-campaign-war -f QEI1
}

function cut_two_edge() {
  cat $1 | cut -c $2- | rev | cut -c $3- | rev
}

function deploy() {
  cmd="mint deploy --config QEI2 -w $1"
  prun $cmd
}

function deploy_withconfig() {
  cmd="mint dev build build-cfg deploy -w $F1 -f QEI2"
  prun $cmd
}

function find_war() {
  _mapff `find /export -name *$1*`
}

function undeflated() {
  perl -MCompress::Zlib -e 'undef $/; print uncompress(<>)'
}

function ts2readable() {
  date -d @$1
}

function nertz_copy_from_magic() {
  cmd="hadoop distcp -D dfs.checksum.type=CRC32 webhdfs://eat1-magicnn01.grid.linkedin.com:50070$1 hdfs://eat1-nertznn01.grid.linkedin.com:9000$2"
  prun $cmd
}

function unjar() {
  if [ ! -f $1 ];
  then
    echo "$1 not exist"
    return 1;
  fi
  base=`basename $1`
  filename="${base%.*}"
  echo $filename
  rm -rf $filename
  mkdir -p $filename
  cp $1 $filename/
  cd $filename
  jar xf $1
  cd ..
}

function _user_do() {
  user=$1
  shift
  cmd="sudo -E -u $user sh -c \"cd ~$user;$*\""
  prun $cmd
}

function unzip_jar() {
  rm -rf zip
  test -e $1 || return 1;
  unzip $1 -d zip
}

function send_bashrc() {
  copy_to $1 ~/.bashrc
}

function biggest_file() {
  find $1 -printf '%s %p\n'| sort -nr | head -50
}

function update_az_ctrl() {
  cp ~/mlutt/az_ctrl.py ~/workspace/tscp-backend_trunk/plugin/
  cp ~/mlutt/az_ctrl.py ~/mlutt/release/
  cp ~/mlutt/az_ctrl.py ~/pip_dist/azkaban_ctrl/azkaban_ctrl/
}

function load_production_fcst_cluster() {
  ssh -t -AL 18882:localhost:18882 eng-portal.corp.linkedin.com 'ssh ela4-app5663.prod.linkedin.com -L 18882:ela4-app5663.prod.linkedin.com:8882'
}

function load_production_fcst_segment_cluster() {
  ssh -t -AL 18089:localhost:18089 eng-portal.corp.linkedin.com 'ssh ela4-app5663.prod.linkedin.com -L 18089:ela4-app5663.prod.linkedin.com:8089'
}

function ssh_add_github() {
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/github_rsa
}

function ssh_add_gitli() {
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/zhdeng_at_linkedin.com_dsa_key
}

function git_list_edit() {
  _mapff `git status | grep -E 'new file:|modified:' | cut -d ':' -f 2`
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
