import sys
import traceback
from flask import *
from util.exceptions import *
from modules.wms.wms_params import *
import modules.plotting.plotting_controller as plotter
import modules.capabilities.capabilities_controller as cap_controller
import config

app = Flask(__name__)

@app.route('/')
def index():
    try:
        params = WMSParams(request.args, config.available).validate()
        
        if params['request'] == 'GetCapabilities':
            defaults = config.capabilities_info
        else:
            defaults = WMSParams(config.defaults).parse()            

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
            
@app.route('/dev')
def dev():
    params = request.args
    return params['styles']

            
def get_capabilities(params, defaults):
    # TODO Should call it like this
    # cap, format = cap_controller.get_capabilities(params, defauts)
    # return render_template("capabilities_1_3_0.xml", cap=cap), format
    cap = cap_controller.get_capabilities(params)
    return render_template("capabilities_1_3_0.xml", cap=cap), 'xml'
        
def handle_exception(exception):
    output = render_template("exceptions_1_3_0.xml", error=exception.data())
    resp = make_response(output)
    resp.headers['Content-Type'] = 'text/xml'
    return resp
    
# TODO shuold use this one after modules return -> content, format
valid_operations = {
    "GetMap": plotter.get_contour,
    "GetFullFigure": plotter.get_full_figure,
    "GetLeyend": plotter.get_legend,
    "GetCapabilities": get_capabilities
    }

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