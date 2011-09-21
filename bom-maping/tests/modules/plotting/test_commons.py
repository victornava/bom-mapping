"""
Unit tests for the commons module
"""
import unittest
import modules.plotting.commons as c
from util.exceptions import BBoxException

class TestBBox(unittest.TestCase):
    
    
    def test_lon_min_greater_lon_max(self):
        bbox = {  "min_lat" : -90.0,
                  "min_lon" : 90.0,
                  "max_lat" : 90.0,
                  "max_lon" : -90.0 }
        self.assertRaises(BBoxException,c.BBox,bbox)
    
    
    def test_lat_min_greater_lat_max(self):
        bbox = {  "min_lat" : 45.0,
                  "min_lon" : -180.0,
                  "max_lat" : -45.0,
                  "max_lon" : 1800.0 }
        self.assertRaises(BBoxException,c.BBox,bbox)
    
    
    def test_lat_min_to_small(self):
        bbox = {  "min_lat" : -91.0,
                  "min_lon" : -180.0,
                  "max_lat" : 90.0,
                  "max_lon" : 180.0 }
        self.assertRaises(BBoxException,c.BBox,bbox)
    
    
    def test_lat_max_to_big(self):
        bbox = {  "min_lat" : -90.0,
                  "min_lon" : -180.0,
                  "max_lat" : 91.0,
                  "max_lon" : 180.0 }
        self.assertRaises(BBoxException,c.BBox,bbox)
    
    
    def test_lon_min_to_small(self):
        bbox = {  "min_lat" : -90.0,
                  "min_lon" : -181.0,
                  "max_lat" : 90.0,
                  "max_lon" : 180.0 }
        self.assertRaises(BBoxException,c.BBox,bbox)
    
    
    def test_lon_max_to_big(self):
        bbox = {  "min_lat" : -90.0,
                  "min_lon" : -180.0,
                  "max_lat" : 90.0,
                  "max_lon" : 361.0 }
        self.assertRaises(BBoxException,c.BBox,bbox)
        """
    def test_normalise_lons1(self):
        bbox = {  "min_lat" : -90.0,
                  "min_lon" : -180.0,
                  "max_lat" : 90.0,
                  "max_lon" : 180.0 }
        bb = c.BBox(bbox)
        self.assertEquals(0.0,bb.lon_min)
        self.assertEquals(360.0, bb.lon_max)
        
    def test_normalise_lons2(self):
        bbox = {  "min_lat" : -90.0,
                  "min_lon" : -160.0,
                  "max_lat" : 90.0,
                  "max_lon" : 160.0 }
        bb = c.BBox(bbox)
        self.assertEquals(0.0,bb.lon_min)
        self.assertEquals(360.0, bb.lon_max)
        """