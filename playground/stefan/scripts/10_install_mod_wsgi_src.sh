#!/bin/bash
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)

if [ "$UID" -ne 0 ] && [ ! -f "/usr/local/bin/python" ] ; then
   echo "You need to run this script as root (su -) and  python 2.7.2 must be installed by hand. Aborting ..."
   exit 1
fi

# We need to make sure httpd-devel is installed

yum install httpd-devel -y

# Let the installation begin

cd /usr/local/src/
wget http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz
tar xvzf mod_wsgi-3.3.tar.gz

cd mod_wsgi-3.3

./configure --with-apxs=/usr/sbin/apxs --with-python=/usr/local/bin/python LD_RUN_PATH=/usr/local/lib/

make -j5
make -j5 install

# Add mod_wsgi to apache

cd /etc/httpd/conf.d

if [ -f "wsgi.conf" ] ; then
   echo "Configuration file for mod_wsgi already exists in /etc/httpd/conf.d. Aborting ..."
   exit 1
fi

echo "LoadModule wsgi_module modules/mod_wsgi.so" > wsgi.conf

echo "Creating direcotry 'wsgi-scripts' under /var/www"

mkdir /var/www/wsgi-scripts 2> /dev/null

# http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIScriptAlias

echo "WSGIScriptAlias /wsgi-scripts/ /var/www/wsgi-scripts/" >> wsgi.conf

echo "Configuration file /etc/httpd/conf.d/wsgi.conf created. This is for testing purposes only. Configure properly for production environment."
