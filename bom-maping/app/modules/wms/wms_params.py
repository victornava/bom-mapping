from util.exceptions import *

class WMSParams():
    """Class for conditioning url parameters before calling the plotting module"""
    def __init__(self, request):
        self.request = request
        
    def to_dict(self):
        """Convert a flask request to dictionary with all keys lowercased"""
        dictionary = {}
        for k in self.request.args.keys():
           dictionary[k.lower()] = self.request.args[k]
        return dictionary
    
    def parse(self):
        """ Parses the http request and translates it to the format
           expected by the plotting controller
        """
        # we define here some common funtions to set the types
        to_list = lambda s: s.split(",")
        bbox = lambda a: dict(zip(["min_lon","min_lat","max_lon","max_lat"], a))
        crs = lambda s: dict(zip(["name","identifier"], s.split(":")))

        # then define a set of rules to apply to each element
        # each rule is a function we will call with the value of key as argument
        rules = { 
           "color_range": [to_list],
           "bbox": [to_list, bbox],
           "crs": [crs],
           "styles": [to_list],
           "layers": [to_list]
        }        
   
        params = self.to_dict()

        # iterate elements and apply the rules if there are any
        # otherwise leave the oritinal parameter
        for key in params:
           if rules.has_key(key):
               for rule in rules[key]:
                   params[key] = rule(params[key])
        
        # return params
        return self.validate(params)
    
    def validate(self, params):
        
        # FIXME pass this as argument to the constructor
        config = {
            "formats": ["png", "jpeg"],
            "operations" : ["GetMap", "GetFullFigure", "GetLeyend", "GetCapabilities"]
        }
        
        # FIXME use put this rules in a dict then iterate
        if "request" not in params.keys():
            raise MissingParameterError("'request' parameter is missing")        
            
        if params['request'] not in config['operations']:
            raise OperationNotSupportedError()
                
        if "format" in params.keys():
            if params["format"] in config["formats"]:
                format = params["format"]
            else:
                raise InvalidFormatError("Format not supported")        
        return params