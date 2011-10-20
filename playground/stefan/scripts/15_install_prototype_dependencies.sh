#!/bin/bash
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)


SRC=/usr/local/src
PYTHON=/usr/local/bin/python
EASY_INSTALL=/usr/local/bin/easy_install
export HDF5_DIR=/usr/local/hdf5
export NETCDF4_DIR=/usr/local/netcdf
export PYTHONPATH=/usr/local/bin:/usr/local/lib/python2.7/site-packages


function install_centos_deps() {
   yum install zlib udunits2-devel curl-devel freetype-devel libpng-devel \
blas-devel lapack-devel atlas gcc-gfortran tk-devel -y
}

function build_hdf() {
   cd $SRC
   wget http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.7.tar.gz
   tar xzvf hdf5-1.8.7.tar.gz
   cd hdf5-1.8.7
   ./configure --prefix=/usr/local/hdf5 --enable-fortran --enable-shared --enable-static --enable-production --enable-hl CFLAGS="-g -fPIC" CXXFLAGS="-g -fPIC" FCFLAGS="-g -fPIC" FFLAGS="-g -fPIC"
   make -j5
   make install
}

function build_netcdf() {
   cd $SRC
   wget http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-4.1.1.tar.gz
   tar xzvf netcdf-4.1.1.tar.gz
   cd netcdf-4.1.1
   ./configure --prefix=/usr/local/netcdf --enable-netcdf4 --enable-cxx-4 --with-libcf --disable-compiler-recover --enable-static --enable-shared --with-pic --enable-separate-fortran --with-hdf5="$HDF5_DIR" --with-udunits CFLAGS="-fPIC -g -O2" CXXFLAGS="-fPIC -g -O2" FCFLAGS="-fPIC -g -O2" FFLAGS="-fPIC -g -O2"
   make -j5
   make install
}

function build_numpy() {
   cd $SRC
   wget http://downloads.sourceforge.net/project/numpy/NumPy/1.6.1/numpy-1.6.1.tar.gz
   tar xzvf numpy-1.6.1.tar.gz
   cd numpy-1.6.1
   $PYTHON setup.py build --fcompiler=gnu95
   $PYTHON setup.py install --prefix=/usr/local
}

function build_scipy() {
   cd $SRC
   wget http://sourceforge.net/projects/scipy/files/scipy/0.9.0/scipy-0.9.0.tar.gz
   tar xzvf scipy-0.9.0.tar.gz
   cd scipy-0.9.0
   $PYTHON setup.py build
   $PYTHON setup.py install --prefix=/usr/local
}

function build_pynetcdf() {
   cd $SRC
   wget http://netcdf4-python.googlecode.com/files/netCDF4-0.9.6.tar.gz
   cd netCDF4-0.9.6
   $PYTHON setup.py install --prefix=/usr/local
}

function build_matplotlib() {
   cd $SRC
   wget http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.0.1/matplotlib-1.0.1.tar.gz
   tar xzvf matplotlib-1.0.1.tar.gz
   cd matplotlib-1.0.1
   # sed necessary to build matplotlib without errors
   sed -i -e 's/Tkinter\.__version__\.split()\[-2\]/Tkinter\.__version__/g' setupext.py
   $PYTHON setup.py build
   $PYTHON setup.py install --prefix=/usr/local
}

function build_basemap() {
   cd $SRC
   wget http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.1/basemap-1.0.1.tar.gz
   tar xzvf basemap-1.0.1.tar.gz
   cd basemap-1.0.1/geos-3.2.0/
   export GEOS_DIR=/usr/local
   ./configure --prefix=$GEOS_DIR 
   make -j5
   make install
   cd ..
   $PYTHON setup.py install --prefix=/usr/local

}

function install_setuptools() {
   cd $SRC
   LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local
   LD_RUN_PATH=/usr/local
   wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz
   tar xzvf setuptools-0.6c11.tar.gz
   cd setuptools-0.6c11
   $PYTHON setup.py build
   $PYTHON setup.py install --prefix=/usr/local
}

function install_pydap() {
   $EASY_INSTALL Paste
   $EASY_INSTALL Pydap
   $EASY_INSTALL pydap.handlers.netcdf
}

install_centos_deps
build_hdf
build_netcdf
build_numpy
build_scipy
build_pynetcdf
build_matplotlib
build_basemap

install_setuptools
install_pydap
