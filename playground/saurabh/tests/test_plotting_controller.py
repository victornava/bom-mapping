"""
Unit tests for the PlottingController Class
"""

import unittest
import modules.plotting.plotting_controller as pc


class TestPlottingController(unittest.TestCase):
    
    def setUp(self):
        self.param = { "bbox" : {  "min_lat" : -90.0,
                                   "min_lon" : 0.0,
                                   "max_lat" : 90.0,
                                   "max_lon" : 360.0 
                                } ,
                        "width" : 300 ,
                        "height" : 400 ,
                        "layers" : ["hr24_prcpa", ] ,
                        "styles" : ["grid", ] ,
                        "crs" : {   "name" : "EPSG" ,
                                    "identifier" : "4283" 
                                } ,
                        "format" : "png" ,
                        "time" : "Default" ,
                        "time_index" : "Default" ,
                        "source_url" : "http://yoursoft06.cs.rmit.edu.au:8001/atmos_latest.nc",
                        "color_range" : (-10,10) ,
                        "n_color" : 10 ,
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
