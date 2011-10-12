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
            "image_formats": ["png", "jpeg"],
            "capabilities_formats": ["xml"],
            "exception_formats": ["xml"],
            "requests" : ["GetMap", "GetFullFigure", "GetLeyend", "GetCapabilities"],
            "styles": ["grid", "contour", "grid_treshold"]
            } 
            
    
    def test_can_parse_a_valid_request(self):
        parsed_subject = WMSParams(self.subject).parse()
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
        parsed_subject = WMSParams(subject).parse()
        for k in target:
            self.assertEquals(target[k], parsed_subject[k])

    def test_validate_with_valid_request(self):
        parsed_subject = WMSParams(self.subject, self.available).validate()
        for k in self.target:
            self.assertEquals(self.target[k], parsed_subject[k])

    def test_validate_with_missing_request(self):
        del(self.subject['request'])
        func = WMSParams(self.subject).validate
        self.assertRaises(MissingParameterError, func)    
     
    def test_validate_with_invalid_request(self):
        self.available = { 'requests' : ["blah"] }
        func = WMSParams(self.subject, self.available).validate
        self.assertRaises(OperationNotSupportedError, func)
        
    def test_validate_image_format(self):
        self.subject['format'] = 'image/png'
        params = WMSParams(self.subject, self.available).validate()
        self.assertEquals('png', params['format'])
             
    def test_error_on_invalid_image_format(self):
        self.subject['format'] = 'image/mp3'
        validate = WMSParams(self.subject, self.available).validate
        self.assertRaises(InvalidFormatError, validate)

    def test_error_on_invalid_capbilities_format(self):
        self.subject['format'] = 'text/weirdformat'
        self.subject['request'] = 'GetCapabilities'
        validate = WMSParams(self.subject, self.available).validate
        self.assertRaises(InvalidFormatError, validate)
            
    def test_validate_with_empty_format(self):
        del(self.subject['format'])
        validate = WMSParams(self.subject, self.available).validate()
        
    def test_parse_custom_variables(self):
        self.subject['custom_levels'] = '0,10, 20'
        self.subject['custom_colors'] = 'red,#202020,b'
        self.subject['custom_min'] = 'cyan'
        self.subject['custom_max'] = 'green'
        parsed_subject = WMSParams(self.subject, self.available).parse()
        self.assertEqual(['0','10','20'], parsed_subject['custom_levels'])
        self.assertEqual(['red','#202020','b'], parsed_subject['custom_colors'])
        self.assertEqual('cyan', parsed_subject['custom_min'])
        self.assertEqual('green', parsed_subject['custom_max'])    
    
if __name__ == '__main__':
    unittest.main()
    