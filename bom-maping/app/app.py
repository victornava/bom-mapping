import sys
from flask import *
from util.exceptions import *
from modules.wms.wms_params import *
import modules.plotting.plotting_controller as plotter
import modules.capabilities.capabilities_controller as cap_controller

app = Flask(__name__)

available = {
    "formats": ["png", "jpeg"],
    "exception_formats": ["xml", "json"],
    "requests" : ["GetMap", "GetFullFigure", "GetLeyend", "GetCapabilities"],
    "styles": ["grid", "contour", "grid_treshold"]
}

defaults = {
    "request":"GetMap",
    "version":"0.0.1",
    "bbox" : "-180,-90,180,90",
    "width" : "256",
    "height" : "256",
    "layers" : "hr24_prcp",
    "styles" : "grid",
    "crs" : "EPSG:4283",
    "format" : "png",
    "time" : "Default",
    "time_index" : "Default",
    "source_url" : "http://localhost:8001/atmos_latest.nc",
    # "source_url" : "http://opendap.bom.gov.au:8080/thredds/dodsC/PASAP/atmos_latest.nc",
    "color_scale_range" : "auto",
    "n_colors" : "7",
    "palette" : "jet"
}

@app.route('/')
def index():
    
    # TODO I could ask the plotting controller for this info
    operations = valid_operations()
    
    try:
        # raise Exception("something terrible wrong")
        params = WMSParams(request, available['requests'], defaults).validate()
        operation = operations[params['request']]
        return operation(params)
    except WMSBaseError, e:
        return handle_exception(e)
    except Exception, e:
        return handle_exception(SomethingWentWrongError("opps!", e))
        
    return handle_exception(exception)
    
def get_map(params):
    """docstring for get_map"""
    img = plotter.get_contour(params)
    resp = make_response(img)
    # TODO change depending on the format parameter
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

    # considering XML as the default output format(MIME Type)
    output_format = 'text/xml'

    # TODO: Decide:- how to respond for an non-supported output format request
    # 1. Handle the request as XML format or 2. Throw an exception
    
    if "format" in params.keys():
        if(params['format'] == 'application/json'):
            output_format = 'application/json'

    if(output_format == 'text/xml'):
        # TODO : Capabilities XML Template
        output = render_template("capabilities_1_3_0.xml", cap=cap)
        resp = make_response(output)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        # TODO : Capabilities JSON Template or look for Flask - Dict to Json
        output = render_template("capabilities_1_3_0.txt", cap=cap)
        resp = make_response(output)
        resp.headers['Content-Type'] = 'application/json'

    return resp

    
def handle_exception(exception):
    """docstring for handle_exception"""
    data = exception.data()
    output = render_template("exceptions_1_3_0.xml", error=data)
    resp = make_response(output)
    resp.headers['Content-Type'] = 'text/xml'
    return resp
    
    
def valid_operations():
    return {
        "GetMap": get_map,
        "GetFullFigure": get_full_figure,
        "GetLeyend": get_leyend,
        "GetCapabilities": get_capabilities
    }
    
    
# TODO  pass optional config file as arg
if __name__ == '__main__':
    port = 8007
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='0.0.0.0', port=port)
