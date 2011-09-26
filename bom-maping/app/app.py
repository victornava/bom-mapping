import sys
from flask import Flask, make_response, request
from modules.wms.wms_params import WMSParams
import modules.plotting.plotting_controller as plotter
import modules.capabilities.capabilities_controller as cap_controller


app = Flask(__name__)

@app.route('/')
def index():
    try:
        params = WMSParams(request).parse()
        # return str(params)
        operations = valid_operations()
        
        if "request" not in params.keys():
            # TODO use appropiate error
            raise ValueError("ServiceException => code:MissingParameter, message:request")
            
        try:
            operation = operations[params['request']]
        except KeyError:
            # TODO use appropiate error
            raise ValueError("ServiceException => code:OperationNotSupported")
            
        return operation(params)
                
    except Exception, e:
        # TODO call WMSException here
        reply = "ServiceException:"+str(e)
        # reply = str(e)
    return reply    
    
def get_map(params):
    """docstring for ge"""
    img = plotter.get_contour(params)
    resp = make_response(img)
    resp.headers['Content-Type'] = 'image/png'
    return resp

def get_full_figure():
    """docstring for get_full_figure"""
    pass
    
def get_leyend():
    """docstring for get_leyend"""
    pass
    
def get_capabilities(params):
    """docstring for get_capabilities"""
    cap = cap_controller.get_capabilities(params)
    resp = make_response(cap)

    # considering XML as the default output format(MIME Type)
    output_format = 'text/xml'

    # TODO: Decide:- how to respond for an non-supported output format request
    # 1. Handle the request as XML format or 2. Throw an exception
    
    if "format" in params.keys():
        if(params['format'] == 'application/json'):
            output_format = 'application/json'

    if(output_format == 'text/xml'):
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp.headers['Content-Type'] = 'application/json'

    return resp

def valid_operations():
    return {
        "GetMap": get_map,
        "GetFullFigure": get_full_figure,
        "GetLeyend": get_leyend,
        "GetCapabilities": get_capabilities
    }

class ServiceException(object):
    """docstring for ServiceException"""
    def __init__(self, arg):
        super(ServiceException, self).__init__()
        self.arg = arg
                    
# can pass the port number as argument
if __name__ == '__main__':
    port = 8007
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='127.0.0.1', port=port)
