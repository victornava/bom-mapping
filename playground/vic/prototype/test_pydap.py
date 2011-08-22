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

url = "http://localhost:8001/ocean_latest.nc"
# 
dataset = open_url(url)
# 
print dataset
# 
