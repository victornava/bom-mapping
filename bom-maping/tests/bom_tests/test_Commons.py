#!/usr/bin/python
"""
Test Module for the Commons Module
"""

import unittest
import bom.Commons as c

class TestPlottingPrams(unittest.TestCase):
    
    def setUp(self):
        self.p = c.PlottingParams()
        
        
class TestBBox(unittest.TestCase):
    """Bounding Box Test"""

    def setUp(self):
        self.b = c.BBox(-50,-100,30,70)
        
    def test_minX(self):
        self.assertEquals(self.b.minX, -50)
        
    def test_minY(self):
        self.assertEquals(self.b.minY,-100)
        
    def test_maxX(self):
        self.assertEquals(self.b.maxX,30)
        
    def test_maxY(self):
        self.assertEquals(self.b.maxY,70)


#class TestMapSize(unittest.TestCase):
#    """ Map Size Test """
    
#    def setUp(self):
#        self.m = c.MapSize(self,150,360)


if __name__ == 'main':
    unittest.main()