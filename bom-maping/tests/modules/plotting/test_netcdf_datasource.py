"""
    Author: Saurabh Pandit(s3270950@student.rmit.edu.au)
    
    Unit tests for NetCDFDatasource module
"""

import unittest
from modules.plotting.datasource import NetCDFDatasource
from util.exceptions import NetCDFException

class TestNetCDFDatasource(unittest.TestCase):
    
    def setUp(self):
        self.d = NetCDFDatasource(
                       'http://yoursoft06.cs.rmit.edu.au:8001/ocean_latest.nc',
                        2,'SsST',4,5,6 )
        
        
    """
        Test if get_lats() returns array of lats
    """
    def test_get_lats(self):
        print "===get_lats==="
        #print self.d.get_lats()
        self.assertIsNotNone(self.d.get_lats())
        
        
    """
        Test if get_lons() returns array of lons
    """
    def test_get_lons(self):
        print "===get_lons==="
        #print self.d.get_lons()
        
        self.assertIsNotNone(self.d.get_lons())
        
    def test_get_data(self):
        print "===get_data==="
        #print self.d.get_data()
        
        with self.assertRaises(NetCDFException):
            
            try:
                self.d.get_data()
            except NetCDFException,e:
                print e.__str__()
                raise
        
        
    def test_get_time_units(self):
        print "===get_time_units==="
        print self.d.get_time_units()
        
        
    def test_get_available_times(self):
        print "===get_available_times==="
        print self.d.get_available_times()
        