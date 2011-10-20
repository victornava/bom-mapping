#!/bin/bash
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)

SRC=/usr/local/src
PYTHON=/usr/local/bin/python
EASY_INSTALL=/usr/local/bin/easy_install

cd
path="/opt/bom-mapping/bom-maping/app"

function install_flask() {
   $EASY_INSTALL Flask
}

function checkout_app() {
   cd /opt
   git clone http://github.com/victornava/bom-mapping.git
   echo "export PYTHONPATH=$path:/usr/local/lib/python2.7/site-packages" >> /etc/profile.d/bom.sh
}

function config_wsgi() {
   cd /etc/httpd/conf.d

   # Add the python path to mod_wsgi
   echo "WSGIPythonPath \"$path\"" >> wsgi.conf
   
}

function create_wsgi_file() {
   NAME="app.wsgi"
   cd /var/www/wsgi-scripts
   # This helps getting over some MPLCOFIG error occuring with mod_wsgi
   echo "import os" > $NAME
   echo "os.environ['MPLCONFIGDIR']='/tmp'" >> $NAME

   echo "from app import app as application" >> $NAME
}

install_flask
checkout_app
config_wsgi
create_wsgi_file
