#.bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

if [ "$(uname)" = Darwin ]; then
  export OS_TYPE=MACOS
else
  export OS_TYPE=LINUX
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
  $HOME.linuxbrew/bin
  $HOME/workspace/kafka-console-consumer
  /export/content/linkedin/bin
  $HOME/package/gradle-2.13/bin
  "

for newPath in $ALL_NEW_PATH
do
  if [ -d $newPath ]; then
    PATH=$PATH:$newPath
  fi
done


if [ "$(type -t rbenv)" = function ]; then eval "$(rbenv init -)"; fi

if [ -x /usr/bin/keychain ] ; then
        eval `keychain --eval --agents ssh github_rsa`
	MYNAME=`/usr/bin/whoami`
	if [ -f ~/.ssh/${MYNAME}_at_linkedin.com_dsa_key ] ; then
	      /usr/bin/keychain ~/.ssh/${MYNAME}_at_linkedin.com_dsa_key
      	      . ~/.keychain/`hostname`-sh
	fi
fi

export EDITOR='vi'
export localhost=127.0.0.1
export HOST_NAME=`cat $HOME/.HOST_NAME`
export WP=$HOME/workspace
export M2_HOME=/usr/local/apache-maven
export M2=$M2_HOME/bin
export TSCPBE=$HOME/workspace/tscp-backend_trunk
export SAS_EI_JDBC='jdbc:oracle:thin:sas/sas8uat@eat1-dc1-eidb-sas.stg.linkedin.com:1521/EI_EIDB_SAS'
export SAS_LOCAL_HOST='localhost:10038/sas-campaign/resources/adCreatives'

# Aquire IP on linux
[ -x /sbin/ip ] && export HOME_IP=`ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'`

# ALIAS ALIAS
alias work='ssh zhdeng@zhdeng-ld1'

if [ $OS_TYPE != MACOS ]; then
  alias ls='ls --color=auto'
fi
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias cls="clear"
alias listjar="ls *.jar | xargs -Ifn sh -c 'echo fn;jar tf fn'"
alias check_port='netstat -lpn'
alias svn='svin'
alias rf='lf'
alias list='list_file'
alias hfs="hadoop fs"
alias wp='cd ~/workspace'
alias network_wp='wp;cd network_trunk'
alias tail_log2='cd_log;tail -f apps.out | grep -v "INFO \[Lix\]" | grep -v "INFO \[ClientAdapter\]" | grep -v "INFO \[ZkBasedSchemaRegistry\]" | grep -v "INFO \[DatabusHttpV3ClientImpl\]"'
alias tail_log='cd_log;tail -f apps.out '
alias tail_doglog='cd /export/content/lid/apps/watchdog-ads-test-service/dev-i001/logs;tail -f watchdog-ads-test-service.out'
alias tail_error_log='cd_log;tail -f apps.out |  grep -n "ERROR"  | grep -v "INFO \[Lix\]"'
alias grep_error_log='cd_log;cat apps.out |  grep -n "ERROR"  | grep -v Lix'
alias grep_warn_log='cd_log;cat apps.out |  grep -E "ERROR|WARN"  | grep -v Lix'
alias tail_tomcat_log='cd_tomcat_log;tail -f catalina.out'
alias kill_fg='kill -9 $(jobs -p)'
alias build_and_release='ligradle build -x test;mint release'
alias build_without_test='ligrade build -x test'
alias jar_list='jar tf '
alias deploy_zookeeper='mint deploy -w zookeeper-war'
alias deploy='deploy.py'
alias bql='bql.py'
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
alias download_autoreview_model='copy_from_gateway.py /jobs/adreview/auto-review/training/model/all/maxent'
alias ligradle_build_xtest='ligradle build -x test --parallel'
alias snapshot_release_x='ligradle_build_xtest; mint release'
alias snapshot_release='snapshot_release_x'
alias patch_a_diff='patch -p0 -i '
alias vimr='vim -R'
alias build_tscp_sasbe='ligradle sasbe:tscp-sasbe-impl:build'
alias stb_assembly='sbt/sbt assembly'
alias eclipse='/export/apps/xtools/eclipse-4.3/eclipse'
alias databus_interactive='$HOME/databus2-cmdline-tools-pkg/bin/dbus2-interactive-avro-schema-gen.sh'
alias su_aaa_roc='mail_chart.py /jobs/adreview/aaa/su-content-model-metrics/_charts'
alias aaa_roc='copy_from_gateway.py /jobs/adreview/aaa/roc-csv ; roc.py /home/zhdeng/incoming/roc-csv/* -i -r 2'
alias sas='sas.py'
alias xopen='xdg-open'
alias weka='cd $HOME/package/weka-3-6-13/;java -Xmx1000M -jar weka.jar'
alias weka_test='java8 -cp ./build/weka-cli/libs/weka-cli-0.0.1-SNAPSHOT.jar:/home/zhdeng/package/weka-3-7-13/weka.jar com.linkedin.weka.SimpleClassifierCli'
alias java8='$HOME/package/jdk1.8.0_51/bin/java'
alias test_single='ligradle test -Dtest.single='
alias gradle='gradle2'

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

function reffrc() {
source ~/.ffrc
}

function bashrc() {
vim ~/.bashrc
cp ~/.bashrc ~/utt/.bashrc
}

function vimrc() {
vim ~/.vimrc
cp ~/.vimrc ~/utt/.vimrc
}

function list_all_build() {
  _mapff `find . -name 'build.gradle'`
}

function motto() {
sort -R ~/motto | head -n 1
}

function nertz() {
  ssh -K eat1-nertzgw01.grid.linkedin.com
}

function holdem() {
  ssh -K ltx1-holdemgw01.grid.linkedin.com
}

function war() {
  ssh -K lva1-wargw01.grid.linkedin.com
}

function portal() {
  ssh -K eng-portal
}

function kill_sth() {
kill `ps aux | grep $1 | grep -v grep | cut -d " " -f 4`
}

function prun() {
  echo $*
  eval "$*"
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

function cut_two_edge() {
  cat $1 | cut -c $2- | rev | cut -c $3- | rev
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

function war_copy_from_nertz() {
  cmd="hadoop distcp hdfs://eat1-nertznn01.grid.linkedin.com:9000$1 hdfs://lva1-warnn01.grid.linkedin.com:9000$2"
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

function load_production_pinot2_controller() {
 ssh  -A -L 11984:localhost:8080 eng-portal.corp.linkedin.com 'ssh lva1-app13279.prod.linkedin.com -L 8080:ltx1-pinot-controller-vip-1.prod.linkedin.com:11984'  
  #print 'http://localhost:11984/query/'
}

function load_production_fcst_cluster() {
  ssh -t -AL 18882:localhost:18882 eng-portal.corp.linkedin.com 'ssh ela4-app5663.prod.linkedin.com -L 18882:ela4-app5663.prod.linkedin.com:8882'
  print 'http://localhost:18882'
}

function load_production_fcst_segment_cluster() {
  ssh -t -AL 18089:localhost:18089 eng-portal.corp.linkedin.com 'ssh ela4-app5663.prod.linkedin.com -L 18089:ela4-app5663.prod.linkedin.com:8089'
  print 'http://localhost:18089'
}

function load_production_bids_cluster() {
  ssh -t -AL 18882:localhost:18882 eng-portal.corp.linkedin.com 'ssh ela4-app7216.prod.linkedin.com -L 18882:ela4-app7216.prod.linkedin.com:8882'
  print 'http://localhost:18882'
}

function load_production_bids_segment_cluster() {
  ssh -t -AL 18089:localhost:18089 eng-portal.corp.linkedin.com 'ssh ela4-app7216.prod.linkedin.com -L 18089:ela4-app7216.prod.linkedin.com:8089'
  print 'http://localhost:18089'
}

function load_production_pacing_cluster() {
  ssh -t -AL 18882:localhost:18882 eng-portal.corp.linkedin.com 'ssh ela4-app6715.prod.linkedin.com -L 18882:ela4-app6715.prod.linkedin.com:8882'
  print 'http://localhost:18882'
}

function proxy_to_schema_registry() {
#ela4-schema-registry-vip-1.prod.linkedin.com:10252/schemaRegistry/schemas
  ssh -t -AL 20252:localhost:20252 eng-portal.corp.linkedin.com 'ssh ela4-schema-registry-vip-1.prod.linkedin.com -L 20252:ela4-schema-registry-vip-1.prod.linkedin.com:10252'
}

function ssh_add_github() {
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/github_rsa
}

function ssh_add_gitli() {
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/zhdeng_at_linkedin.com_dsa_key
}

function portal_run() {
  cmd="ssh -q -K -tt eng-portal \"$*\""
  prun $cmd
}

function build_vim_java_imports() {
  #find "$HOME/workspace" | grep build |  grep -e ".classpath$"  | xargs cat | tr ':' '\n' | sort | uniq | tr '\n' ':' > ~/vim/JavaImp/jars
  find "$HOME" | grep build |  grep -e ".classpath$"  | xargs cat | tr ':' '\n' | sort | uniq | tr '\n' ':' > ~/vim/JavaImp/jars
}

function listen_to_ei_kafka() {
if [ $# -lt 1 ]; then
  echo "listen_to_ei_kafka topic"
  return 1
fi
echo "listening... " $1
kafka-console-consumer.sh --zookeeper zk-ei2-kafka.stg:12913/kafka-cluster-aggregate --topic $1 --property schema.registry.url=http://eat1-ei2-schema-vip-z.stg.linkedin.com:10252/schemaRegistry/schemas
}

function listen_to_ei_kafka1() {
if [ $# -lt 1 ]; then
  echo "listen_to_ei_kafka[1|2] topic"
  return 1
fi
echo "listening... " $1
kill_sth "kafka-console-consumer"
kafka-console-consumer.sh --zookeeper zk-ei1-kafka.stg:12913/kafka-cluster --topic $1 --property schema.registry.url=http://eat1-schema-vip-z.stg.linkedin.com:10252/schemaRegistry/schemas
}

function listen_to_ei_kafka2() {
if [ $# -lt 1 ]; then
  echo "listen_to_ei_kafka[1|2] topic"
  return 1
fi
echo "listening... " $1
kill_sth "kafka-console-consumer"
kafka-console-consumer.sh --zookeeper zk-ei2-kafka.stg:12913/kafka-cluster --topic $1 --property schema.registry.url=http://eat1-ei2-schema-vip-z.stg.linkedin.com:10252/schemaRegistry/schemas
}

function pinot_hosts() {
  #app-status -fg prod -t pinot-senseidb.ads-click
  app-status -fg prod  pinot-senseidb
}

function pinot2_hosts() {
  if [ $# -lt 2 ]; then
    echo "ex: pinot2_hosts prod-lva1 scin-forecast"
    return 1
  fi
  app-status -f $1 pinot-server | egrep "`eh -u %prod-lva1.pinot20-$2:SERVER | sed 's/,/|/g'`"
}

function pinot2_broker() {
  if [ $# -lt 2 ]; then
    echo "ex: pinot2_broker prod-lva1 scin-forecast"
    return 1
  fi
  eh -e %$1.pinot20-$2:BROKER
}

function compile_avro_schema() {
  java -jar ~/javajar/avro-tools-1.4.0.jar compile schema $1 databus-events/databus-events/src/main/java/ 
}


function app_status() {
  app-status -fg prod $1
}

function mint_dependency_update() {
  mint dependency update --product=$F1
}

function sshtomachine() {
  ssh-range -f $1 -m $2 $3
}

function copySasbeSnapshot() {
  cp $1 ../tscp-api_trunk/tscp-sasbe-api/src/main/snapshot
}
function copySasbeIdl() {
  cp $1 ../tscp-api_trunk/tscp-sasbe-api/src/main/idl
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

# Disable F1
#xmodmap -e 'keycode 67='
alias cd_forecast='wp;cd forecast_trunk'
alias cd_opennlp='wp;cd opennlp'
alias cd_ingraph='wp;cd ingraphs'
alias cd_spark='cd $HOME/spark'
alias cd_money_spark='wp; cd money-spark'
alias cd_mlutt='cd $HOME/mlutt'
alias cd_admm='cd $HOME/ars-admm_trunk'
alias cd_adsutt='cd $HOME/adsutt'
alias cd_adsrel='wp;cd ads-relevance_trunk'
alias cd_tscp='wp;cd tscp_trunk'
alias cd_admin='wp;cd tscp-admin-backend_trunk'
alias cd_admin_prod='cd $HOME/prod/tscp-admin-backend_trunk'
alias cd_admin2='wp;cd tscp-admin-backend_trunk2'
alias cd_admin3='wp;cd tscp-admin-backend_trunk3'
alias cd_tscp_targeting='wp;cd tscp-targeting_trunk'
alias cd_tscp_tracking='wp;cd tscp-tracking_trunk'
alias cd_be='wp;cd tscp-backend_trunk'
alias cd_tscpbe='wp;cd tscp-backend_trunk'
alias cd_api='wp;cd tscp-api_trunk'
alias cd_tscp_api='wp;cd tscp-api_trunk'
alias cd_tscpbe_prod='wp;cd $HOME/prod/tscp-backend_trunk'
alias cd_tscp_prod='wp;cd $HOME/prod/tscp_trunk'
alias cd_tscpbe2='wp; cd tscp-backend_trunk2'
alias cd_tscpbe_lib='wp;cd $HOME/tscp-backend_trunk_lib'
alias cd_tscp_frontend='wp;cd tscp-admin-frontend_trunk'
alias cd_tracker='wp;cd tracker_trunk'
alias cd_ucf='wp;cd ucf_trunk'
alias cd_bam='wp;cd bam_trunk'
alias cd_bam_api='wp;cd bam-api_trunk'
alias cd_bam_offline='wp;cd recls; cd bam-offline'
alias cd_bam_ev='wp;cd evaluator;'
alias cd_pinot='wp;cd pinot-hadoop_trunk;'
alias cd_autoapprove='wp;cd autoadapprovalmlmodel;'
alias cd_autoreview='cd $HOME/auto-review;'
alias cd_metronome='wp;cd metronome_trunk'
alias cd_liar='network_wp; cd liar/'
alias cd_liar_hadoop='wp; cd liar-hadoop_trunk/'
alias cd_lame='network_wp; cd liar/lame/java/com/linkedin/liar/lame/'
alias cd_az='wp; cd azkaban'
alias cd_pig='wp; cd pig'
alias cd_avro='wp; cd avro'
alias cd_avro_schemas='wp; cd avro-schemas_trunk'
alias cd_avsc='wp; cd avro-schemas_trunk'
alias cd_liarloser='network_wp; cd liar/loser/java/com/linkedin/liar/'
alias cd_loser='wp; cd loser_trunk'
alias cd_csp_impl='network_wp; cd sasbe/cspserving-impl'
alias cd_sas='network_wp; cd sas'
alias cd_sasbe='network_wp; cd sasbe'
alias cd_network='network_wp;'
alias cd_network2='wp; cd network_trunk2;'
alias cd_recls='wp;cd recls'
alias cd_recls_prod='cd $HOME/prod/recls'
alias cd_schemas='wp;cd avro-schemas_trunk'
alias cd_log='cd /export/content/lid/apps/apps/dev-i001/logs'
alias cd_tomcat_log='cd /export/content/lid/apps/tomcat/dev-i001/logs'
alias cd_fcst_log='cd /export/content/lid/apps/forecasting-service/dev-i001/logs'
alias cd_fcst_war='cd $HOME/local-repo/com/linkedin/forecast/forecasting-service-war'
alias cd_chimera='wp;cd chimera_trunk'
alias cd_insight='wp;cd insight'
alias cd_uscp='wp;cd uscp_trunk'
alias cd_pegasus='wp;cd pegasus_trunk'
alias cd_common_template='wp;cd common-templates'
alias cd_pdsc='wp;cd pegasus_trunk'
alias cd_model='wp; cd models_trunk'
alias cd_arda_frontend='wp; cd arda-frontend'
alias cd_databus_event='wp; cd databus-events_trunk'
alias cd_databus2='wp; cd databus2_trunk'
alias cd_ucv='wp; cd content-validation-api_trunk'
alias cd_security='wp; cd security_trunk'
alias cd_domain='wp; cd network_trunk/domain/'
alias cd_crc='wp; cd content-relevance-classifiers-server_trunk/'
alias cd_r='cd $HOME/R'
alias cd_weka_hadoop='wp; cd weka-hadoop_trunk'
alias cd_laser='wp; cd laser_trunk'
alias cd_laser8='wp; cd laser8_trunk'
alias cd_ufs='wp; cd forecasting-service_trunk'
alias cd_lax='wp; cd lax-service_trunk'
alias cd_weka='cd $HOME/package/weka-3-6-13'
alias cd_metronome_examples='wp; cd metronome-examples_trunk' 
alias cd_container='wp; cd container_trunk' 
alias cd_metrics='wp; cd metric-defs_trunk' 
alias cd_ads_topic='wp; cd ads-topic'
alias cd_pip_dist='cd $HOME/pip_dist'
alias cd_ff='cd $HOME/pip_dist/ff'
alias cd_fire_spark='wp; cd fire-spark'
alias cd_watch_dog='wp; cd watchdog-ads-test-service_trunk'
