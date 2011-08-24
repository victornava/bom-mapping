#!/bin/bash
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)

# install general dependencies
yum install zlib udunits2-devel curl-devel freetype-devel libpng-devel blas-devel lapack-devel atlas gcc-gfortran tk-devel -y

# install gcc devel environment
yum groupinstall 'Development Tools' -y

# install git
yum install git-all -y
