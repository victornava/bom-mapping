#!/bin/bash
# Based on: http://pydap.org/server.html#running-pydap-with-apache
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)

mkdir /var/www/pydap 2> /dev/null

cd
mkdir src 2> /dev/null
cd src
wget http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.6.4.tar.gz
tar xzvf virtualenv-1.6.4.tar.gz
cd virtualenv-1.6.4
python virtualenv.py --no-site-packages /var/www/pydap/env
#python virtualenv.py --no-site-packages /var/www/pydap/env
source /var/www/pydap/env/bin/activate
easy_install Paste
easy_install Pydap
easy_install pydap.handlers.netcdf
cd /
paster create -t pydap /var/www/pydap/server

# add options to pydap config file
cd /var/www/pydap/server/apache/

echo "Modifying /var/www/pydap/server/apache/pydap.wsgi ..."
echo "import site" > pydap.new
echo "site.addsitedir('/var/www/pydap/env/lib/python2.7/site-packages')" >> pydap.new
echo "" >> pydap.new
cat pydap.wsgi >> pydap.new

mv pydap.new pydap.wsgi

# now edit apache files

echo "Modifying /etc/httpd/conf.d/wsgi.conf ..."
cd /etc/httpd/conf.d/
echo "" >> wsgi.conf
echo "WSGIScriptAlias /pydap /var/www/pydap/server/apache/pydap.wsgi" >> wsgi.conf
echo "" >> wsgi.conf
echo "<Directory /var/www/pydap/server/apache>" >> wsgi.conf
echo "    Order allow,deny" >> wsgi.conf
echo "    Allow from all" >> wsgi.conf
echo "</Directory>" >> wsgi.conf

echo "Done"
echo ""
