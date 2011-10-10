""" This module contains common datatypes need in the plotting module 

Author: Stefan Fuchs (s3260968@student.rmit.edu.au)
"""
import util.exceptions as ex

class BBox(object):
    """ Represents a bounding box """
    
    def __init__(self,bbox):
        """ Constructor
        bbox: {
                min_lat: string
                min_lon: string
                max_lat: string
                max_lon: string
                }
        """
        expected_keys = ['min_lon', 'min_lat', 'max_lon', 'max_lat']
        
        # Check that keys exist
        for key in expected_keys:
            if not bbox.has_key(key):
                raise ex.MissingDimensionValueError("Missing value in" \
                                                    "Bounding Box")
        try:
            bbox = dict([(k,float(v)) for k,v in bbox.items()])
        except Exception, e:
            raise ex.InvalidDimensionValueError("Invalid bbox parameter.")
        
        self.lon_min = bbox["min_lon"]
        self.lat_min = bbox["min_lat"]
        self.lon_max = bbox["max_lon"]
        self.lat_max = bbox["max_lat"]
        
#        if self.lon_min < -180.0:
#            raise ex.InvalidDimensionValueError("min_lon (" + \
#                                                str(self.lon_min) +\
#                                                ") too small.")
        
#        if self.lon_max > 360.0:
#            raise ex.InvalidDimensionValueError("max_lon (" + \
#                                                str(self.lon_max) +\
#                                                ") too big.")
        
#        if self.lat_min < -90.0:
#            raise ex.InvalidDimensionValueError("min_lat (" + \
#                                                str(self.lat_min) + \
#                                                ") too small.")
                                                
#        if self.lat_max > 90.0:
#            raise ex.InvalidDimensionValueError("max_lat (" + \
#                                                str(self.lat_max) + \
#                                                ") too big.")
       
        if self.lon_min > self.lon_max:
            raise ex.InvalidDimensionValueError("min_lon greater than max_lon")
        
        if self.lat_min > self.lat_max:
            raise ex.InvalidDimensionValueError("min_lat greater than max_lat")