#!/bin/bash
# Execute this script as root
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)

if [ "$UID" -ne 0 ] ; then
   echo "You need to run this script as root (su -), or we can't install python 2.7.2 to /usr/local ... Aborting"
   exit 1
fi

cd /usr/local/src
wget http://python.org/ftp/python/2.7.2/Python-2.7.2.tar.bz2
tar xvjf Python-2.7.2.tar.bz2
cd Python-2.7.2

./configure --prefix=/usr/local --with-fpectl --enable-shared --with-libc="" --with-pth --with-system-ffi LDFLAGS="-Wl,-rpath /usr/local/lib"

make -j5
make -j5 install

# create symlink for shared libraries
# fix from: http://code.google.com/p/modwsgi/wiki/InstallationIssues

cd /usr/local/lib/python2.7/config
ln -s ../../libpython2.7.so .
