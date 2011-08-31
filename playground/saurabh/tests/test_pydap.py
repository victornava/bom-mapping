# import httplib2
# from pydap.util import socks
# import pydap.lib

# pydap.lib.PROXY = httplib2.ProxyInfo(
#     socks.PROXY_TYPE_HTTP,
#     'host,
#     8080,
#     proxy_user='user',
#     proxy_pass='password'
# )

import sys
import site

site.addsitedir("/root/bom-epd/epd/lib/python2.7/site-packages")
from pydap.client import open_url

# url = "http://localhost:8001/coads.nc"
#url = "http://localhost:8001/test.csv"
url = "http://yoursoft06.cs.rmit.edu.au:8001/ocean_latest.nc"
# url = "http://yoursoft06.cs.rmit.edu.au:8001/coads.nc"
# 
dataset = open_url(url)
# 
print dataset
# 
