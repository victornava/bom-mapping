#!/bin/bash
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)


# install general dependencies
function prototype_general_deps() {
   yum install zlib udunits2-devel curl-devel freetype-devel libpng-devel blas-devel lapack-devel atlas gcc-gfortran tk-devel -y
}

# install gcc devel environment
function install_dev_tools() {
   yum groupinstall 'Development Tools' -y
}

# install git
function install_git() {
   yum install git-all -y
}

#install firefox for testing purposes
function install_user_tools() {
   yum install firefox -y
}


#prototype_general_deps
#install_dev_tools
install_git
#install_user_tools
