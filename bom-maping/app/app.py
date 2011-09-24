import sys
from flask import Flask, make_response, request
from modules.wms.wms_params import WMSParams
import modules.plotting.plotting_controller as plotter

app = Flask(__name__)

@app.route('/')
def index():
    try:
        params = WMSParams(request).parse()
        # return str(params)
        ops = operations()
        
        if not params.has_key("request"):
            # TODO use appropiate error
            raise ValueError("ServiceException => code:MissingParameter, message:request parameter is missing")
            
        try:
            operation = ops[params['request']]
        except KeyError:
            raise ValueError("ServiceException => code:OperationNotSupported")
            
        return operation(params)
                
    except Exception, e:
        # TODO call WMSException here
        reply = str(e)
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
    
def get_capabilities():
    """docstring for get_capabilities"""
    pass

def operations():
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
    app.run(host='0.0.0.0', port=port)


        
        