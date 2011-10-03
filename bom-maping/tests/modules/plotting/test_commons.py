"""
Unit tests for the commons module.

Author: Stefan Fuchs (s3260968@student.rmit.edu.au)
"""
import unittest
import modules.plotting.commons as c
import util.exceptions as ex

class TestBBox(unittest.TestCase):
    """ Class containing tests for the Bounding Box class """
    
    def setUp(self):
        self.bbox = { "min_lat" : "-90.0",
                      "min_lon" : "0" ,
                      "max_lat" : "90.0" ,
                      "max_lon" : "360.0" }
    
    
    # 1. Parameters are not specified as numbers
    def test_min_lat_no_number(self):
        self.bbox["min_lat"] = "-90.a"
        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
        
    def test_min_lon_no_number(self):
        self.bbox["min_lon"] = "6asd6"
        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
        
    def test_max_lat_no_number(self):
        self.bbox["max_lat"] = "wa6sd"
        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
        
    def test_max_lon_no_number(self):
        self.bbox["max_lon"] = "as34df"
        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
        
        
    # 2. Parameters missing
    def test_min_lat_missing(self):
        del self.bbox["min_lat"]
        self.assertRaises(ex.MissingDimensionValueError,c.BBox,self.bbox)
        
    def test_min_lon_missing(self):
        del self.bbox["min_lon"]
        self.assertRaises(ex.MissingDimensionValueError,c.BBox,self.bbox)
        
    def test_max_lat_missing(self):
        del self.bbox["max_lat"]
        self.assertRaises(ex.MissingDimensionValueError,c.BBox,self.bbox)
        
    def test_max_lon_missing(self):
        del self.bbox["max_lon"]
        self.assertRaises(ex.MissingDimensionValueError,c.BBox,self.bbox)
        
        
    # 3. Parameters are ourside of their range
#    def test_min_lat_to_small(self):
#        self.bbox["min_lat"] = "-90.1"
#        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
    
#    def test_max_lat_to_big(self):
#        self.bbox["max_lat"] = "90.1"
#        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
        
#    def test_min_lon_to_small(self):
#        self.bbox["min_lon"] = "-180.1"
#        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
        
#    def test_max_lon_to_big(self):
#        self.bbox["max_lon"] = "360.1"
#        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
    
    
    # 4. Valid parameters
    def test_boundary_values(self):
        c.BBox(self.bbox)
        
    def test_normal_values(self):
        self.bbox["min_lat"] = "-80.3253234"
        self.bbox["max_lat"] = "45.123"
        self.bbox["min_lon"] = "-45.233232423"
        self.bbox["max_lon"] = "23.1234234324"
        c.BBox(self.bbox)
    
    
    # 5. Longitudes/Latitudes are not overlapping
    def test_min_lat_greater_max_lat(self):
        self.bbox["min_lat"] = "45.8"
        self.bbox["max_lat"] = "-18.2"
        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)
        
    def test_min_lon_greater_max_lon(self):
        self.bbox["min_lon"] = "150.3"
        self.bbox["max_lon"] = "50.4"
        self.assertRaises(ex.InvalidDimensionValueError,c.BBox,self.bbox)