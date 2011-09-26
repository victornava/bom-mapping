"""
    Author: Saurabh Pandit(s3270950@student.rmit.edu.au)
    
    Unit tests for NetCDFDatasource module
"""

import unittest
from modules.plotting.datasource import NetCDFDatasource
from util.exceptions import NetCDFException
from modules.plotting.commons import BBox


class TestDatasource(unittest.TestCase):
    
    def setUp(self):
        self.bbox = BBox({  "min_lat" : -90.0,
                            "min_lon" : 0.0,
                            "max_lat" : 90.0,
                            "max_lon" : 360.0
                        })
        
        self.d = NetCDFDatasource(
                       'http://yoursoft06.cs.rmit.edu.au:8001/atmos_latest.nc',
                        self.bbox,
                        'hr24_prcp')
        
        
    """
        Test if get_lats() returns array of lats
    """
    def test_get_lats(self):
        print "===get_lats==="
        print self.d.get_lats()
        self.assertIsNotNone(self.d.get_lats())
        
        
    """
        Test if get_lons() returns array of lons
    """
    def test_get_lons(self):
        print "===get_lons==="
        print self.d.get_lons()
        
        self.assertIsNotNone(self.d.get_lons())
        
    def test_get_data(self):
        print "===get_data==="
        #print self.d.get_data()
        
        #with self.assertRaises(NetCDFException):
        self.d = NetCDFDatasource(
                       'http://yoursoft06.cs.rmit.edu.au:8001/ocean_latest.nc',
                        self.bbox,
                        'SSTA_cc', plot_mask = False)
        try:
            print self.d.get_data()
        except NetCDFException,e:
            print e.__str__()
            raise
        
        
    def test_get_time_units(self):
        print "===get_time_units==="
        print self.d.get_time_units()
        
        
    def test_get_available_times(self):
        print "===get_available_times==="
        print self.d.get_available_times()
        
        
    def test_get_var_unit(self):
        print "===get_var_units==="
        
        self.d = NetCDFDatasource(
                       'http://yoursoft06.cs.rmit.edu.au:8001/ocean_latest.nc',
                        self.bbox,
                        'SSTA_cc')
        
        print self.d.get_var_unit()
        
        
    def test_get_time_label(self):
        print "===get_time_label==="
        
        self.d = NetCDFDatasource(
                       'http://yoursoft06.cs.rmit.edu.au:8001/ocean_latest.nc',
                        self.bbox,
                        'SSTA_cc')
        
        print self.d.get_time_label()
