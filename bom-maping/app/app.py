import sys
from flask import Flask, make_response, request
from modules.wms.wms_params import WMSParams

app = Flask(__name__)

@app.route('/')
def index():
    
    try:
        params = WMSParams(request).parse()
        # TODO call plotting module here
        reply = str(params) 
    except Exception, e:
        # TODO call WMSException here
        reply = str(e)    
    return reply
        
# can pass the port number as argument
if __name__ == '__main__':
    port = 8007
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='0.0.0.0', port=port)


        
        