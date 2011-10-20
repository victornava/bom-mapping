"""
    Author: Saurabh Pandit(s3270950@student.rmit.edu.au)
    
    Unit tests for NetCDFDatasource module
"""

import unittest
from modules.plotting.datasource import NetCDFDatasource
import util.exceptions as ex
from modules.plotting.commons import BBox
import os


class TestDatasource(unittest.TestCase):
    
    def setUp(self):
        self.bbox = BBox({  "min_lat" : -82.0,
                            "min_lon" : -85.0,
                            "max_lat" : 86.0,
                            "max_lon" : 87.0
                        })
        """
        self.d = NetCDFDatasource(
                       '/home/saurabh/Downloads/atmos_latest.nc',
                        self.bbox,
                        'hr24_prcp')
        """
        self.d = NetCDFDatasource(
                       '/atmos_latest.nc',
                        self.bbox,
                        'hr24_prcp')
        
    """
        1. Test if datasource raises error for relative url.
    """
    def test_relative_url_error(self):
        print "===Relative Url Error==="
        #Should raise an error for relative url
        self.assertRaises(ex.InvalidParameterValueError, \
                    NetCDFDatasource, \
                    '/../../../../../../../saurabh/Downloads/atmos_latest.nc',\
                    self.bbox, 'SSTA_cc', plot_mask=True)
        
        # No back slash at the start of the file name
        self.assertRaises(ex.InvalidParameterValueError, \
                    NetCDFDatasource, \
                    'atmos_latest.nc',\
                    self.bbox, 'SSTA_cc', plot_mask=True)
        
        
    """
        1. Test if get_lats() returns array of lats
    """
    def test_get_lats(self):
        print "===get_lats==="
        print self.d.get_lats()
        self.assertIsNotNone(self.d.get_lats())
        
        
    """
        2. Test if get_lats() returns LayerNotDefinedError for varname which 
    """
    def test_get_latitudes(self):
        print "===get_lats for invalid_layer==="
        self.d = NetCDFDatasource('http://opendap.jpl.nasa.gov/opendap/' + \
                            'GeodeticsGravity/tellus/L3/eof_ocean_mass/' + \
                            'netcdf/GRC_CSR_RL04_DPC_OCN_eofr_200302_201103.nc',
                        self.bbox,
                        'Water_Thickness')
        print self.assertRaises(ex.LayerNotDefinedError, self.d.get_lats)
        
    """
        3. Test if get_lons() returns array of lons
    """
    def test_get_lons(self):
        print "===get_lons==="
        print self.d.get_lons()
        
        #self.assertRaises(None, self.d.get_lons)
        
    """
        3. Test if data is retrieved with right url, bbox params, varname
    """
    def test_get_data(self):
        print "===get_data==="
        
        self.d = NetCDFDatasource(
                       '/ocean_latest.nc',
                        self.bbox,
                        'SST',
                        plot_mask = False)
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
                          NetCDFDatasource, \
                          '/wrong/ocean_latest.nc', \
                          self.bbox, 'SSTA_cc', plot_mask=True)
        
    """
        5. Test if constructor raises LayerNotDefinedError error with
        wrong varname
    """
    def test_layer_not_found_error(self):
        print "===Layer not found error==="
        
        self.d = NetCDFDatasource(
                       '/atmos_latest.nc',
                        self.bbox,
                        'invalid_layer')
        
        self.assertRaises(ex.LayerNotDefinedError, \
                            self.d.get_data)
        try:
            self.d.get_data()
        except Exception,e:
            print e.__str__()
            
    """
        6. Test if constructor raises InvalidParameterValueError error with
        wrong varname
    
    def test_bbox_param(self):
        print "===bbox param error==="
        self.bbox = BBox({  "min_lat" : -90.0,
                            "min_lon" : -180.0,
                            "max_lat" : 80.0,
                            "max_lon" : 360.0
                        })
        self.d = NetCDFDatasource(
                       'http://yoursoft06.cs.rmit.edu.au:8001/atmos_latest.nc',
                        self.bbox,
                        'hr24_prcp')
                        
        self.assertRaises(Exception, \
                            self.d.get_data)
        #try:
        self.d.get_data()
        #except Exception,e:
        #    print e.__str__()
    """
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
            self.d = NetCDFDatasource(
                    '/ocean_latest.nc',
                    self.bbox,
                    'SSTA_cc')
            print self.d.get_var_unit()
        except ex.InvalidParameterValueError,e:
            print e.__str__(), " ===> Manual printing error"
       