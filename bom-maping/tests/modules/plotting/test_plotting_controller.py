"""
Unit tests for the PlottingController Class
"""

import unittest
import modules.plotting.plotting_controller


class TestPlottingController(unittest.TestCase):
    
    def setUp(self):
        self.param["bbox"] = {  "min_lat" : -90.0,
                                "min_lon" : -180.0,
                                "max_lat" : 90.0,
                                "max_lon" : 180.0 }
        self.param["width"] = 300
        self.param["height"] = 400
        self.param["layers"] = ["hr24_prcp", ]
        self.param["styles"] = ["contour", ]
        self.param["crs"] = { "name" : "EPSG",
                              "identifier" : "4283" }
        self.param["format"] = "png"
        self.param["time"] = "Default"
        self.param["time_index"] = "Default"
        self.param["source_url"] = "http://localhost:8001/atmos_latest.nc"
        self.param["color_range"] = (-4,4)
        self.param["n_color"] = 10
        self.param["palette"] = "jet"