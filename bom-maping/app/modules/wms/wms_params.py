class WMSParams():
    
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
        each_to_int = lambda a: [int(elem) for elem in a]
        # each_to_float = lambda a: [float(elem) for elem in a]
        bbox = lambda a: dict(zip(["min_lon","min_lat","max_lon","max_lat"], a))
        crs = lambda s: dict(zip(["name","identifier"], s.split(":")))
        
        # then define a set of rules to apply to each element
        # each rule is a function we will call with the value of key as argument
        rules = { 
            "color_range" : [to_list, each_to_int],
            "height": [int],
            "width": [int],
            "n_color": [int],
            "bbox": [to_list, bbox],
            "crs": [crs],
            "styles": [to_list],
            "layers": [to_list]
        }
        
        # lowercase all the keys
        # params = dict([(k.lower(),v) for k,v in self.to_dict().items()])
            
        params = self.to_dict()
        
        # iterate elements and apply the rules if there are any
        for key in params:
            if rules.has_key(key):
                for rule in rules[key]:
                    try:
                        params[key] = rule(params[key])
                    except Exception, e:
                        # TODO throw meaninful exception
                        raise ValueError("Error parsing parameter: "+key)
        return params

# class WMSParamsError(Exception):
#     """docstring for WMSParamsError"""
#     def __init__(self, arg):
#         super(WMSParamsError, self).__init__()
#         self.arg = arg