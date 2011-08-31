#! /bin/ksh
# Builds the numerical, plotting and scientific libraries needed
# for PASAP web served products, against python 2.4.3 for RHEL 5
# This involves building netCDF4 (and its deps).
# Order is important to satisfiy dependencies.
# The order simply follows the order of functions in this script.

# DEPENDENCIES ON OS PACKAGES
# zlib -- required for hdf/netcdf
# udunits2-devel.x86_64
# curl-devel (libcurl -- required for building dap enabled netCDF4.)
# freetype-devel -- required for matplotlib
# libpng-devel -- required for matplotlib
# blas-devel --required for scipy, good for numpy
# lapack-devel -- required for scipy, good for numpy
# atlas -- makes scipy faster
# gfortran
# python-devel

# tk-devel -- required for matplotlib?
# Scroll to the end for the block of code that calls the individual build
# functions Yes, I thought about using make for this, but shell was a bit
# quicker to get up and running.

# Download virtual-python.py from setuptools web site
# run python virtual-python.py --prefix=
# Download pip tarball.
# install pip
# add pip to path
# pip install virtualenv --install-option"--prefix=...path"

# pip install simplejson
# must remove pydap's __init__.py to use pip, and then add it again. .... 

# www.python.org/download/releases/2.4.6
# Andrew Charles March 2011

src=/home/acharles/src
cd $src
print $LD_LIBRARY_PATH
PREFIX=/home/acharles/local/python/2.4.3
export PYTHONPATH=/home/acharles/local/python/2.4.3/bin:/home/acharles/python_tools:/home/acharles/local/python/2.4.3/lib/python2.4/site-packages:/home/acharles/local/python/2.4.3/lib64/python2.4/site-packages:/usr/lib/python2.4/site-packages

function create_paths {
    mkdir /home/acharles/local/python
    mkdir /home/acharles/local/hdf
    mkdir /home/acharles/local/netcdf
    mkdir /home/acharles/local/python/2.4.3
}

function install_virtual {
    tar -xvzf virtualenv-1.5.2.tar.gz
    mv virtualenv-1.5.2/virtualenv.py /home/acharles
    python /home/acharles/virtualenv.py /home/acharles/local/python/2.4.3
}

function build_hdf {
    export HDF5_DIR=/home/acharles/local/hdf
    tar -zxvf hdf5-1.8.5-patch1.tar.gz
    cd hdf5-1.8.5-patch1
    ./configure --prefix=/home/acharles/local/hdf5/1.8.5-patch1 --enable-fortran --enable-shared --enable-static --enable-production --enable-hl --enable-linux-lfs CFLAGS="-g -fPIC" CXXFLAGS="-g -fPIC" FFLAGS="-g -fPIC" FCFLAGS="-g -fPIC"
    print `pwd`
    make -j4
    #make check
    make install
    cd ..
}

function build_netcdf {
    tar -xvzf netcdf-4.1.1.tar.gz 
    cd netcdf-4.1.1
    ./configure --prefix=/home/acharles/local/netcdf/4.1.1 --enable-netcdf-4 --enable-cxx-4 --with-libcf --enable-separate-fortran --enable-docs-install --disable-compiler-recover --enable-static --enable-shared --enable-dap --with-pic --with-hdf5=/opt/hdf5/1.8.5-patch1 --with-udunits=/opt/udunits2 CFLAGS="-fPIC -g -O2" CXXFLAGS="-fPIC -g -O2" FFLAGS="-fPIC -g -O2" FCFLAGS="-fPIC -g -O2"
    make -j4
    #make check
    make install
    cd ..
}

python=/usr/bin/python

function install_setuptools {
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PREFIX
    print $LD_LIBRARY_PATH
    LD_RUN_PATH=$PREFIX
    # Makes installing some other packages a bit easier...
    # run as an egg, see http://pypi.python.org/pypi/setuptools
    # Requires python2.6 on your path, or aliased in .bashrc
    #sh setuptools-0.6c11-py2.6.egg --prefix=/opt/python/2.6.4
    tar -xvzf setuptools-0.6c11.tar.gz
    cd setuptools-0.6c11
    $python setup.py build
    print $PYTHONPATH
    $python setup.py install --prefix=$PREFIX
    cd ..
}


function build_pip {
    tar -xvzf pypa-pip-0.8.3-13-gcb0d835.tar.gz
    cd pypa-pip-cb0d835
    $python setup.py build
    $python setup.py install --prefix=$PREFIX
    cd ..
}

#function build_atlas {
#    print 'nothing to see here'
#
#}

function build_numpy {
    # We can do better than this - what about atlas, etc...
    # There's a chance this won't be an optimally fast build of numpy.
    # NB this is a higher version than on twister, which is 1.3
    # but scipy 0.8 requires numpy 1.4 or higher
    tar -xvzf numpy-1.5.1.tar.gz
    cd numpy-1.5.1
    $python setup.py build --fcompiler=gnu95
    $python setup.py install --prefix=$PREFIX
    cd ..
}

function build_scipy {
    # Scipy not actually required for PASAP, so not built for now
    # NB this fails because no BLAS
    # if want to link to specific BLAS, LAPACK, ATLAS use
    # export BLAS=...path
    # export LAPACK=path
    # export ATLAS=path
    tar -xvzf scipy-0.8.0.tar.gz
    cd scipy-0.8.0
    $python setup.py build
    $python setup.py install --prefix=$PREFIX
    cd ..
}

function build_pynetcdf {
    # python-netcdf4 build without opendap support. Use pydap for this.
    tar -xvzf netCDF4-0.9.3.tar.gz
    cd netCDF4-0.9.3
    export NETCDF4_DIR=/home/acharles/local/netcdf/4.1.1
    export HDF5_DIR=/home/acharles/local/hdf5/1.8.5-patch1
    $python setup.py install --prefix=$PREFIX
    # Run tests in test directory using python run_all.py
}

easyinstall=/home/acharles/local/python/2.4.3/bin/easy_install

function build_pydap {
    # We don't have the source, we use easy_install to download it
    # In fact this seems to be the only documented install method...
    pip install Pydap -E /home/acharles/local/python/2.4.3/bin/python
    #$easyinstall Paste --prefix=$PREFIX --install-dir=$PREFIX
    #$easyinstall Pydap --prefix=$PREFIX --install-dir=$PREFIX
}

function build_ipython {
    $easyinstall readline
    $easyinstall ipython 
}

function build_matplotlib {
    #sudo yum install freetype-devel
    #sudo yum install libpng-devel
    tar -xvzf matplotlib-1.0.1.tar.gz
    cd matplotlib-1.0.1
    $python setup.py build
    $python setup.py install --prefix=$PREFIX
    # TEST!!???
    cd ..
}

function build_basemap {
    tar -xvzf basemap-1.0.1.tar.gz
    cd basemap-1.0.1
    cd geos-3.2.0
    export GEOS_DIR=/opt/geos/3.2.0
    ./configure --prefix=$GEOS_DIR
    make
    make install
    cd ..
    $python setup.py install --prefix=$PREFIX
}

#create_paths
#install_virtual
#build_ipython
#build_hdf
#build_netcdf
#build_numpy
#build_scipy
#build_pynetcdf
#build_matplotlib
#build_pydap
#build_basemap






