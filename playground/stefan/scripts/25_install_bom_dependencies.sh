#!/bin/bash
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)

SRC=/usr/local/src
PYTHON=/usr/local/bin/python
EASY_INSTALL=/usr/local/bin/easy_install

function install_flask() {
   $EASY_INSTALL Flask
}

install_flask
