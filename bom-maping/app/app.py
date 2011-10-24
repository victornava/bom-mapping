import sys
import traceback
from flask import *
from util.exceptions import *
from modules.wms.wms_params import *
from modules.wms.helpers import *
import modules.plotting.plotting_controller as plotter
import modules.capabilities.capabilities_controller as cap_controller
import config

app = Flask(__name__)

@app.route('/')
def index():
    try:
        params = WMSParams(request.args, config.available).validate()
        
        # FIXME: hack to work around styles parameter conflicts with test client
        if 'plot_styles' in params:
            params['styles'] = [params['plot_styles']]
        
        if params['request'] == 'GetCapabilities':
            defaults = config.capabilities_defaults
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
    # return "blah"
    params = request.args
    return params['format']

            
def get_capabilities(params, defaults):
    cap,format = cap_controller.get_capabilities(params,defaults)
    return render_template("capabilities_1_3_0.xml", cap=cap), format
        
def handle_exception(exception):
    output = render_template("exceptions_1_3_0.xml", error=exception.data())
    resp = make_response(output)
    resp.headers['Content-Type'] = 'text/xml'
    return resp
    
valid_operations = {
    "GetMap": plotter.get_contour,
    "GetFullFigure": plotter.get_full_figure,
    "GetLegend": plotter.get_legend,
    "GetCapabilities": get_capabilities
    }

# if __name__ == '__main__':
#    port = 8007
#    if len(sys.argv) > 1:
#        port = int(sys.argv[1])
#    
#    #TODO remember to turn off before going live
#    app.debug = True
#    # app.debug = False
#    app.run(host='0.0.0.0', port=port)
