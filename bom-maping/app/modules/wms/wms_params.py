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
        each_to_float = lambda a: [float(elem) for elem in a]
        # bbox = lambda a: dict(zip(["min_lat","min_lon","max_lat","max_lon"], a))
        bbox = lambda a: dict(zip(["min_lon","min_lat","max_lon","max_lat"], a))
        crs = lambda s: dict(zip(["name","identifier"], s.split(":")))
        
        # then define a set of rules to apply to each element
        # each rule is a function we will call with the value of key as argument
        rules = { 
            "color_range" : [to_list, each_to_int],
            "height": [int],
            "width": [int],
            "n_color": [int],
            "bbox": [to_list, each_to_float, bbox],
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
                        raise ValueError("Error parsing parameter: "+key)
        return params

# class WMSParamsError(Exception):
#     """docstring for WMSParamsError"""
#     def __init__(self, arg):
#         super(WMSParamsError, self).__init__()
#         self.arg = arg
        
    
            
class FakeRequest():
    """Fake Flask Request for testing. Expects a dict as argument"""
    
    def __init__(self, args):
        self.args = args
    
    def get(self, key):
        return self.args[key]
    
    def keys(self):
        return self.args.keys()

######################################################
# tests
######################################################
import unittest

class TestWMSParams(unittest.TestCase):
    def test_to_dict(self):
        params = {'a':'1', 'b':'2'}
        request = FakeRequest(params)
        d = WMSParams(request).to_dict()
        self.assertEquals(params, d)
    
    def test_parse(self):
        subject = {
            "request":"GetMap",
            "version":"0.0.1",
            "bbox" : "-90.0,-180.0,90.0,180.0",
            "width" : "300",
            "height" : "400",
            "layers" : "hr24_prcp",
            "styles" : "contour",
            "crs" : "EPSG:4283",
            "format" : "png",
            "time" : "default",
            "time_index" : "default",
            "source_url" : "http://localhost:8001/atmos_latest.nc",
            "color_range" : "-4,4",
            "n_color" : "10",
            "palette" : "jet"
        }
        target = {
            "request":"GetMap",
            "version": "0.0.1",
            "bbox" : {
                "min_lat": -90.0,
                "min_lon": -180.0,
                "max_lat": 90.0,
                "max_lon": 180.0
            },
            "width" : 300,
            "height" : 400,
            "layers" : ["hr24_prcp"],
            "styles" : ["contour"],
            "crs" : {
                "name":"EPSG",
                "identifier":"4283"
            },
            "format" : "png",
            "time" : "default",
            "time_index" : "default",
            "source_url" : "http://localhost:8001/atmos_latest.nc",
            "color_range" : [-4,4],
            "n_color" : 10,
            "palette" : "jet"
        }
        parsed_subject = WMSParams(FakeRequest(subject)).parse()
        for k in target:
            self.assertEquals(target[k], parsed_subject[k])        
    

class TestFakeRequest(unittest.TestCase):
    def test_get(self):
        params = {'a':'1', 'b':'2'}
        fake_request = FakeRequest(params)
        self.assertEquals(fake_request.get('a'), '1')
        self.assertEquals(fake_request.get('b'), '2')
        
    def test_args(self):
        params = {'a':'1', 'b':'2'}
        self.assertEquals(FakeRequest(params).args, params)
    
    def test_keys(self):
        params = {'a':'1', 'b':'2'}
        self.assertEquals(FakeRequest(params).args.keys(), ['a','b'])
        
        
if __name__ == '__main__':
    unittest.main()