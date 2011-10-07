from util.exceptions import *

class WMSParams():
    """Class for conditioning url parameters before calling the plotting module"""
    def __init__(self, request, available={}):
        self.request = request
        self.available = available
        self.parse()
    
    def to_dict(self):
        """Convert a flask request to dictionary with all keys lowercased"""
        dictionary = {}
        for k in self.request.args.keys():
           dictionary[k.lower()] = self.request.args[k]
        self.dict = dictionary
        return self.dict
    
    
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
           "color_scale_range": [to_list],
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
        
        # remove the image/ part from image/png
        if 'format' in params: 
            format = params['format'].split("/")
            params['format'] = format[len(format)-1]
        
        # return params
        self.dict = params
        return self.dict
    
    
    def validate(self):
        if "request" not in self.dict:
            raise MissingParameterError("'request' parameter is missing")        

        if self.dict['request'] not in self.available['requests']:
            raise OperationNotSupportedError("operation '" +self.dict['request']+"' is not supported")
        
        # Handle capabilities format especial case
        msg = "Format '" +self.dict["format"]+"' not supported for request '" + self.dict['request']
        if self.dict['request'] == 'GetCapabilities':
            if self.dict["format"] not in self.available['capabilities_formats']:
                raise InvalidFormatError(msg)
        elif self.dict["format"] not in self.available['image_formats']:
            raise InvalidFormatError(msg)
        
        return self.dict