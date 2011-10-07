import sys
import traceback
from flask import *
from util.exceptions import *
from modules.wms.wms_params import *
import modules.plotting.plotting_controller as plotter
import modules.capabilities.capabilities_controller as cap_controller

app = Flask(__name__)

available = {
    "formats": ["png", "jpeg"],
    "image_formats": ["png", "jpeg"],
    "capabilities_formats": ["xml"],
    "exception_formats": ["xml"],
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
    try:
        params = WMSParams(request, available).validate()
        fn = valid_operations[params['request']]
        content, format = fn(params, defaults)
        response = make_response(content)
        response.headers['Content-Type'] = content_type_for(format)
        return response
    except WMSBaseError, e:
        return handle_exception(e)
    except Exception, e:
        if app.debug == True:
            # let flask show the exception
            raise e
        else:
            return handle_exception(SomethingWentWrongError("Sorry.", e))
            
def get_capabilities(params, defaults):
    # TODO Should call it like this
    # cap, format = cap_controller.get_capabilities(params, defauts)
    # return render_template("capabilities_1_3_0.xml", cap=cap), format
    cap = cap_controller.get_capabilities(params)
    return render_template("capabilities_1_3_0.xml", cap=cap), "xml"
    
def get_map(params, defaults):
    # TODO Should call it like this
    # return plotter.get_contour(params, defaults)
    return plotter.get_contour(params), defaults['format']
    
def get_full_figure(params, defaults):
    # TODO Should call it like this
    # return plotter.get_full_figure(params, defaults)
    return plotter.get_full_figure(params), defaults['format']
    
def get_legend(params, defaults):
    # TODO Should call it like this
    # return plotter.get_legend(params, defaults)
    return plotter.get_legend(params), defaults['format']
    
def handle_exception(exception):
    output = render_template("exceptions_1_3_0.xml", error=exception.data())
    resp = make_response(output)
    resp.headers['Content-Type'] = 'text/xml'
    return resp

valid_operations = {
    # make alias in plotter to get contour 
    "GetMap": get_map,
    "GetFullFigure": get_full_figure,
    "GetLeyend": get_legend,
    "GetCapabilities": get_capabilities
    }

# TODO shuold use this one after modules return -> content, format
# valid_operations = {
#     # make alias in plotter to get contour 
#     "GetMap": plotter.get_contour,
#     "GetFullFigure": plotter.get_full_figure,
#     "GetLeyend": plotter.get_legend,
#     "GetCapabilities": get_capabilities
#     }

def content_type_for(format):
    format = format.lower()
    if format in ['png', 'jpg', 'svg']:
        return "image/"+format 
    elif format in ['xml', 'html', 'json', 'txt']:
        return "text/"+format
    else:
        raise InvalidFormatError("Don't know how to set content type for: " + str(format));
    
# TODO  pass optional config file as arg
if __name__ == '__main__':
    port = 8007
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    # TODO remember to turn off before going live
    app.debug = True
    # app.debug = False
    app.run(host='0.0.0.0', port=port)