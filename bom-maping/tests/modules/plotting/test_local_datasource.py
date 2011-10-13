"""
    Author: Saurabh Pandit(s3270950@student.rmit.edu.au)
    
    Unit tests for LocalNetCDFDatasource module
"""

import unittest
from modules.plotting.datasource import LocalNetCDFDatasource
import util.exceptions as ex
from modules.plotting.commons import BBox


class TestDatasource(unittest.TestCase):
    
    def setUp(self):
        self.bbox = BBox({  "min_lat" : -90.0,
                            "min_lon" : -80.0,
                            "max_lat" : 90.0,
                            "max_lon" : 80.0
                        })
        
        self.d = LocalNetCDFDatasource(
                       '/home/saurabh/Downloads/atmos_latest.nc',
                        self.bbox,
                        'hr24_prcp')
        
        
    """
        1. Test if get_lats() returns array of lats
    """
    def test_get_lats(self):
        print "===get_lats==="
        print self.d.get_lats()
        self.assertIsNotNone(self.d.get_lats())
        
        
    """
        2. Test if get_lons() returns array of lons
    """
    def test_get_lons(self):
        print "===get_lons==="
        print self.d.get_lons()
        
        self.assertIsNotNone(self.d.get_lons())
        
    """
        3. Test if data is retrieved with right url, bbox params, varname
    """
    def test_get_data(self):
        print "===get_data==="
        
        self.d = LocalNetCDFDatasource(
                       '/home/saurabh/Downloads/ocean_latest.nc',
                        self.bbox,
                        'SST', plot_mask = False)
        try:
            print self.d.get_data()
        except Exception,e:
            print e.__str__()
            raise
        
    """
        4. Test if constructor raises InvalidParameterValueError error with
        wrong url.
    """
    def test_url_error(self):
        print "===get_data Url Error==="
        
        self.assertRaises(ex.InvalidParameterValueError, \
                          LocalNetCDFDatasource, \
                          '/wrong/ocean_latest.nc', \
                          self.bbox, 'SSTA_cc', plot_mask=True)
        
    """
        5. Test if constructor raises LayerNotDefinedError error with
        wrong varname
    """
    def test_layer_not_found_error(self):
        print "===Layer not found error==="
        
        self.d = LocalNetCDFDatasource(
                       '/home/saurabh/Downloads/atmos_latest.nc',
                        self.bbox,
                        'invalid_layer')
        
        self.assertRaises(ex.LayerNotDefinedError, \
                            self.d.get_data)
        try:
            self.d.get_data()
        except Exception,e:
            print e.__str__()
            
    """
        6. 
    """
    def test_bbox_param(self):
        print "===bbox param error==="
        self.bbox = BBox({  "min_lat" : -90.0,
                            "min_lon" : -180.0,
                            "max_lat" : 80.0,
                            "max_lon" : 360.0
                        })
        self.d = LocalNetCDFDatasource(
                       '/home/saurabh/Downloads/atmos_latest.nc',
                        self.bbox,
                        'hr24_prcp')
                        
        self.assertRaises(Exception, \
                            self.d.get_data)
        try:
            print self.d.get_data()
        except Exception,e:
            print e.__str__()
        
    def test_get_time_units(self):
        print "===get_time_units==="
        print self.d.get_time_units()
        
        
    def test_get_available_times(self):
        print "===get_available_times==="
        print self.d.get_available_times()
        
        
    def test_get_var_unit(self):
        print "===get_var_units==="
        
        #with self.assertRaises(ex.InvalidUrlError):
        try:
            print "+++++contruct+++++"
            self.d = LocalNetCDFDatasource(
                    '/home/saurabh/Downloads/ocean_latest.nc',
                    self.bbox,
                    'SSTA_cc')
            print self.d.get_var_unit()
        except ex.InvalidParameterValueError,e:
            print e.__str__(), " ===> Manual printing error"
            
        
        
    def test_get_time_label(self):
        print "===get_time_label==="
        
        #print self.d.get_time_label()