from modules.wms.wms_params import WMSParams
from util.exceptions import *
import unittest

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
            "color_scale_range" : "auto",
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
            "color_scale_range" : ["auto"],
            "n_colors" : ["10"],
            "palette" : "jet"
            }
        
        self.available = {
                "formats": ["png", "jpeg"],
                "image_formats": ["png", "jpeg"],
                "capabilities_formats": ["xml"],
                "exception_formats": ["xml"],
                "requests" : ["GetMap", "GetFullFigure", "GetLeyend", "GetCapabilities"],
                "styles": ["grid", "contour", "grid_treshold"]
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
            
    def test_validate_with_valid_request(self):
        request = FakeRequest(self.subject)
        parsed_subject = WMSParams(request, self.available).validate()
        for k in self.target:
            self.assertEquals(self.target[k], parsed_subject[k])
            
    def test_validate_with_missing_request(self):
        del(self.subject['request'])
        request = FakeRequest(self.subject)
        func = WMSParams(request).validate
        self.assertRaises(MissingParameterError, func)    
    
    def test_validate_with_invalid_request(self):
        request = FakeRequest(self.subject)
        self.available = { 'requests' : ["blah"] }
        func = WMSParams(request, self.available).validate
        self.assertRaises(OperationNotSupportedError, func)
        
    def test_validate_image_format(self):
        self.subject['format'] = 'image/png'
        request = FakeRequest(self.subject)
        params = WMSParams(request, self.available).validate()
        self.assertEquals('png', params['format'])
        
    def test_error_on_invalid_image_format(self):
        self.subject['format'] = 'image/mp3'
        request = FakeRequest(self.subject)
        validate = WMSParams(request, self.available).validate
        self.assertRaises(InvalidFormatError, validate)
    
    def test_error_on_invalid_capbilities_format(self):
        self.subject['format'] = 'text/weirdformat'
        self.subject['request'] = 'GetCapabilities'
        request = FakeRequest(self.subject)
        validate = WMSParams(request, self.available).validate
        self.assertRaises(InvalidFormatError, validate)

class FakeRequest():
    """Fake Flask Request for testing. Expects a dict as argument"""

    def __init__(self, args):
        self.args = args

    def get(self, key):
        return self.args[key]

    def keys(self):
        return self.args.keys()
            

class TestFakeRequest(unittest.TestCase):
    def setUp(self):
        self.params = {'a':'1', 'b':'2'}
    
    def test_get(self):
        fake_request = FakeRequest(self.params)
        self.assertEquals(fake_request.get('a'), '1')
        self.assertEquals(fake_request.get('b'), '2')
        
    def test_args(self):
        self.assertEquals(FakeRequest(self.params).args, self.params)
    
    def test_keys(self):
        self.assertEquals(FakeRequest(self.params).args.keys(), ['a','b'])
        
if __name__ == '__main__':
    unittest.main()