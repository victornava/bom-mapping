#!/bin/sh
# Installation SCRIP for pasp prototype, based on Anrew Charles Script
# Install dependencies on CentOS 5.6 :
#   yum install zlib udunits2-devel curl-devel freetype-devel libpng-devel blas-devel lapack-devel atlas gcc-gfortran python-devel tk-devel
#   yum groupinstall 'Development Tools'
# Stefan Fuchs

# Variables

CCFLAGS="-fPIC -g"
PYTHON=/usr/bin/python
EASYINSTALL=/home/bom/local/python/2.4.3/bin/easy_install

# Script

src=~/src

echo "Starting installation"
#mkdir $src
#cd $src

PREFIX=/home/$USER/local/python/2.4.3
export PYTHONPATH=/home/$USER/local/python/2.4.3/bin:/home/$USER/python_tools:/home/$USER/local/python/2.4.3/lib/python2.4/site-packages:/home/$USER/local/python/2.4.3/lib64/python2.4/site-packages:/usr/lib/python2.4/site-packages

# Functions

function create_paths() {
   mkdir -p ~/local/python
   mkdir -p ~/local/hdf
   mkdir -p ~/local/netcdf
   mkdir -p ~/local/python/2.4.3
}

function install_virtual() {
   echo "Installing virtualenv-1.6.4"
   cd ~/packages
   tar xzf virtualenv-1.6.4.tar.gz
   mv virtualenv-1.6.4/virtualenv.py ~
   python ~/virtualenv.py ~/local/python/2.4.3
   
}

function build_hdf() {
   echo "Building HDF5"
   cd ~/packages
   export HDF5_DIR=~/local/hdf
   tar xzf hdf5-1.8.6.tar.gz
   cd hdf5-1.8.6
   ./configure --prefix="/home/$USER/local/hdf5/1.8.6" --enable-fortran --enable-shared --enable-static --enable-production --enable-hl --enable-linux-lfs CFLAGS="$CCFLAGS" CXXFLAGS="$CCFLAGS" FFLAGS="$CCFLAGS" FCFLAGS="$CCFLAGS"
   make -j5
   make install
}

function build_netcdf() {
   echo "Build NetCDF 4"
   cd ~/packages
   tar xzf netcdf-4.1.1.tar.gz
   cd netcdf-4.1.1
   ./configure --prefix=/home/$USER/local/netcdf/4.1.1 --enable-netcdf-4 --enable-cxx-4 --with-libcf --enable-separate-fortran --enable-docs-install --disable-compiler-recover --enable-static --enable-shared --enable-dap --with-pic --with-hdf5=/home/bom/local/hdf5/1.8.6 --with-udunits CFLAGS="$CCFLAGS -O2" CXXFLAGS="$CCFLAGS -O2" FFLAGS="$CCFLAGS -O2" FCFLAGS="$CCFLAGS -O2"
   make -j5
   make install
}

function build_setuptools() {
   echo "Building setuptools"
   cd ~/packages
   LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PREFIX
   LD_RUN_PATH=$PREFIX
   tar xzf setuptools-0.6c11.tar.gz  
   cd setuptools-0.6c11
   $PYTHON setup.py build
   echo $PYTHONPATH
   $PYTHON setup.py install --prefix=$PREFIX   
}

function build_pip() {
   echo "Build PIP"
   cd ~/packages
   tar xzf pypa-pip-1.0.2-0-gea60bb7.tar.gz
   cd pypa-pip-81b1ef6/
   $PYTHON setup.py build
   $PYTHON setup.py install --prefix=$PREFIX
}

function build_numpy() {
   echo "Building numpy"
   cd ~/packages
   tar xzf numpy-1.6.1.tar.gz
   cd numpy-1.6.1
   $PYTHON setup.py build -fcompiler=gnu95
   $PYTHON setup.py install --prefix=$PREFIX
}

function build_scipy() {
   echo "Building scipy"
   cd ~/packages
   tar xzf scipy-0.9.0.tar.gz
   cd scipy-0.9.0
   $PYTHON setup.py build
   $PYTHON setup.py install --prefix=$PREFIX
}

function build_pynetcdf() {
   echo "Building pynetcdf"
   cd ~/packages
   tar xzf netCDF4-0.9.6.tar.gz
   cd netCDF4-0.9.6
   export NETCDF4_DIR=/home/$USER/local/netcdf/4.1.1
   export HDF5_DIR=/home/$USER/local/hdf5/1.8.6
   $PYTHON setup.py install --prefix=$PREFIX
}

function build_pydap() {
   echo "Building Pydap"
   export PATH=$PATH:/home/$USER/local/python/2.4.3/bin
   pip install Pydap -E /home/$USER/local/python/2.4.3/bin/python
}

function build_ipython() {
   echo "Building iPython"
   echo $PYTHONPATH
   echo $PREFIX
   #$EASYINSTALL -d $PREFIX/lib/python2.4/site-packages readline
   # newest version doesnt work with python 2.4
   $EASYINSTALL -d $PREFIX/lib/python2.4/site-packages ipython==0.10.2
}

function build_matplotlib() {
   echo "Building Matplotlib"
   cd ~/packages
   tar xzf matplotlib-1.0.1.tar.gz
   cd matplotlib-1.0.1
   $PYTHON setup.py build
   $PYTHON setup.py install --prefix=$PREFIX
}

function build_basemap() {
   echo "Building Basemap"
   cd ~/packages
   tar xzf basemap-1.0.1.tar.gz
   cd basemap-1.0.1
   cd geos-3.2.0
   export GEOS_DIR=~/geos-3.2.0
   ./configure --prefix=$GEOS_DIR
   make -j5
   make install
   cd ..
   $PYTHON setup.py install --prefix=$PREFIX
}


# Script calling functions

create_paths
install_virtual
build_hdf
build_netcdf
build_setuptools
build_pip
build_numpy
build_scipy
build_pynetcdf
build_pydap
build_ipython
build_matplotlib
build_basemap

echo "\n\nDone"
