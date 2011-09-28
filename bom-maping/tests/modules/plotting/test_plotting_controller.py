"""
Unit tests for the PlottingController Class

Author: Stefan Fuchs (s3260968@student.rmit.edu.au)
"""
import unittest
import modules.plotting.plotting_controller as pc
import util.exceptions as ex


class TestPlottingController(unittest.TestCase):
    
    def setUp(self):
        self.param = { "bbox" : {  "min_lat" : "-90.0",
                                   "min_lon" : "0.0",
                                   "max_lat" : "90.0",
                                   "max_lon" : "360.0" 
                                } ,
                        "width" : "300" ,
                        "height" : "400" ,
                        "layers" : ["hr24_prcpa", ] ,
                        "styles" : ["grid", ] ,
                        "crs" : {   "name" : "EPSG" ,
                                    "identifier" : "4283" 
                                } ,
                        "format" : "png" ,
                        "time" : "Default" ,
                        "time_index" : "Default" ,
                        "source_url" : "http://localhost:8001/atmos_latest.nc",
                        "color_scale_range" : ["-10", "10"] ,
                        "n_colors" : "10" ,
                        "palette" : "jet"
                     }

        
    def test_get_contour(self):
        c = pc.PlottingController(self.param)
        self.assertIsNotNone(c.get_contour())
        
#    def test_get_legend(self):
#        c = pc.PlottingController(self.param)
#        self.assertIsNotNone(c.get_legend())
        
#    def test_get_full_figure(self):
#        c = pc.PlottingController(self.param)
#        self.assertIsNotNone(c.get_full_figure)


class TestParameterValidator(unittest.TestCase):
    
    def setUp(self):
        self.param = { "bbox" : {  "min_lat" : "-90.0",
                                   "min_lon" : "0.0",
                                   "max_lat" : "90.0",
                                   "max_lon" : "360.0" 
                                } ,
                        "layers" : ["hr24_prcpa", ] ,
                        "styles" : ["grid", ] ,
                        "crs" : {   "name" : "EPSG" ,
                                    "identifier" : "4283" 
                                } ,
                        "width" : "300" ,
                        "height" : "400" ,
                        "format" : "png" ,
                        
                        "time" : "Default" ,
                        "time_index" : "Default" ,
                        "source_url" : "http://localhost:8001/atmos_latest.nc",
                        "color_scale_range" : ["-10", "10", ] ,
                        "n_colors" : ["10", ] ,
                        "palette" : "jet"
                     }
    
    # 1) Check when everything is valid
    def test_all_valid(self):
        v = pc.ParameterValidator(self.param)
        v.validate()
    
    
    # 2) Test for absence of mandatory parameters
    def test_missing_bbox(self):
        del self.param["bbox"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_layers(self):
        del self.param["layers"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_styles(self):
        del self.param["styles"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_crs(self):
        del self.param["crs"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_height(self):
        del self.param["height"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_width(self):
        del self.param["width"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_format(self):
        del self.param["format"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_source_url(self):
        del self.param["source_url"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_color_scale_range(self):
        del self.param["color_scale_range"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
    def test_missing_number_of_colors(self):
        del self.param["n_colors"]
        v = pc.ParameterValidator(self.param)
        self.assertRaises(ex.MissingParameterError, v.validate )
        
        
    # 3) Check if correct value is assigned if optional parameter is missing
    def test_missing_time(self):
        del self.param["time"]
        v = pc.ParameterValidator(self.param)
        v.validate()
        self.assertEquals(self.param["time"],"Default")
        
    def test_missing_time_index(self):
        del self.param["time_index"]
        v = pc.ParameterValidator(self.param)
        v.validate()
        self.assertEquals(self.param["time_index"],"Default")
        
    def test_missing_palette(self):
        del self.param["palette"]
        v = pc.ParameterValidator(self.param)
        v.validate()
        self.assertEquals(self.param["palette"],"jet")