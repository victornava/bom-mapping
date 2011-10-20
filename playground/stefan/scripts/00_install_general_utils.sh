#!/bin/bash
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)

# set up config files
function prepare_centos_config() {

# set yum.conf to only download packages for appropriate architecture
grep "multilib_policy" /etc/yum.conf 2> /dev/null 1>&2
if [ "$?" -eq 1 ] ; then
   echo "Adding \"multilib_plicy=best\" to /etc/yum.conf"
   echo "multilib_policy=best" >> /etc/yum.conf
else
  echo "\"multilib_policy\" already set."
fi
sleep 2

# Add epel repo to /etc/yum.repos.d
cd /etc/yum.repos.d/
REPO="epel.repo"
ls /etc/yum.repos.d/ | grep "epel.repo" 2> /dev/null 1>&2
if [ "$?" -eq 1 ] ; then
   echo "Adding \"$REPO\" to /etc/yum.conf.d/"
   echo '[EPEL]' > $REPO
   echo 'name=Extra Packages for EL 5 - $basearch' >> $REPO
   echo 'mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=epel-5&arch=$basearch' >> $REPO
   echo 'gpgkey=http://download.fedora.redhat.com/pub/epel/RPM-GPG-KEY-EPEL' >> $REPO
   echo 'gpgcheck=1' >> $REPO
   echo 'enabled=1' >> $REPO
else
   echo "\"$REPO\" already exists."
fi
sleep 2

}

# install general dependencies
function prototype_general_deps() {
   echo "Installing OS dependencies"
   sleep 2
   yum install zlib udunits2-devel curl-devel freetype-devel libpng-devel \
blas-devel lapack-devel atlas gcc-gfortran tk-devel -y
}

# install gcc devel environment
function install_dev_tools() {
   echo "Installing Development Tools"
   sleep 2
   yum groupinstall 'Development Tools' -y
}

# install git
function install_git() {
   echo "Installing GIT"
   sleep 2
   yum install git-all -y
}

#install firefox for testing purposes
function install_user_tools() {
   echo "Installing user tools"
   sleep 2
   yum install firefox -y
}

prepare_centos_config
prototype_general_deps
install_dev_tools
install_git
#install_user_tools
