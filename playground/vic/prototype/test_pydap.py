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

site.addsitedir("/Library/Python/2.6/site-packages")
from pydap.client import open_url

# url = "http://localhost:8001/coads.nc"
# url = "http://yoursoft06.cs.rmit.edu.au/ocean_latest.nc"
url = "http://yoursoft06.cs.rmit.edu.au:8001/coads.nc"
# 
dataset = open_url(url)
# 
print dataset
# 
