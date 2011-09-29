from modules.wms.wms_params import WMSParams
import unittest

class FakeRequest():
    """Fake Flask Request for testing. Expects a dict as argument"""
    
    def __init__(self, args):
        self.args = args
    
    def get(self, key):
        return self.args[key]
    
    def keys(self):
        return self.args.keys()

class TestWMSParams(unittest.TestCase):
    
    def setUp(self):
        self.subject = {
            "request":"GetMap",
            "version":"0.0.1",
            "bbox" : "-180.0,-90.0,180.0,90.0",
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
            "n_colors" : "10",
            "palette" : "jet"
            }
        
        self.target = {
            "request":"GetMap",
            "version": "0.0.1",
            "bbox" : {
                "min_lon": "-180.0",
                "min_lat": "-90.0",
                "max_lon": "180.0",
                "max_lat": "90.0",
            },
            "width" : "300",
            "height" : "400",
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
            "color_range" : ["-4","4"],
            "n_colors" : ["10"],
            "palette" : "jet"
            }
                
    def test_to_dict(self):
        params = {'a':'1', 'b':'2'}
        request = FakeRequest(params)
        d = WMSParams(request).to_dict()
        self.assertEquals(params, d)
    
    def test_can_parse_a_valid_request(self):
        parsed_subject = WMSParams(FakeRequest(self.subject)).parse()
        for k in self.target:
            self.assertEquals(self.target[k], parsed_subject[k])        
            
    def test_can_parse_bbox_with_missing_values(self):
        subject = {"bbox" : "-180.0,-90.0,180.0"}
        target = {
            "bbox" : {
                "min_lon": "-180.0",
                "min_lat": "-90.0",
                "max_lon": "180.0"
            }
        }
        parsed_subject = WMSParams(FakeRequest(subject)).parse()
        for k in target:
            self.assertEquals(target[k], parsed_subject[k])
            
    def test_validate_with_valid_parameters(self):        
        subject = self.subject
        target = self.target
        context = {"operations": ["GetMap", "GetCapabilities"]}
        request = FakeRequest(subject)
        parsed_subject = WMSParams(request, context).validate()
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