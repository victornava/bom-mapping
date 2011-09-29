from util.exceptions import *
from modules.wms.validator import *

class WMSParams():
    """Class for conditioning url parameters before calling the plotting module"""
    def __init__(self, request, context=None):
        self.request = request
        self.context = context
        
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
           "layers": [to_list],
           "n_colors": [to_list]
        }        
   
        params = self.to_dict()

        # iterate elements and apply the rules if there are any
        # otherwise leave the oritinal parameter
        for key in params:
           if rules.has_key(key):
               for rule in rules[key]:
                   params[key] = rule(params[key])
        
        return params
        # return self.validate(params)
    
    def validate(self):
        params = self.parse();  
        operations = self.context['operations']   
        ensure("request").is_in(params).orRaise(MissingParameterError("request")).run()
        ensure(params["request"]).is_in(operations).orRaise(OperationNotSupportedError(params["request"])).run()
        return params
        
    # def validate(self):
    #     params = self.parse();  
    #     operations = self.context['operations']
    #     
    #     if "request" not in params.keys():
    #         raise MissingParameterError("'request' parameter is missing")        
    # 
    #     if params['request'] not in operations:
    #         raise OperationNotSupportedError("operation '" +params['request']+"' is not supported")
    #     
    #     return params
