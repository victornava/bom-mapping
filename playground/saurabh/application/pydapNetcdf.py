#!/usr/bin/python

from pydap.client import open_url


def printContent(key,nc_file):
    #print key
    print nc_file[key][0:10]


url = 'http://localhost:8001/atmos_latest.nc'

ncfile = open_url(url)

keys = ncfile.keys()

for k in keys:
    printContent(k,ncfile)