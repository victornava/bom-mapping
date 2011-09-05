#!/usr/bin/python

from pydap.client import open_url

url = 'http://localhost:8001/ocean_latest.nc'

ncfile = open_url(url)

print ncfile.keys()