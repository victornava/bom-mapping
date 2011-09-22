""" This module contains common datatypes need in the plotting module """

from util.exceptions import BBoxException

class BBox(object):
    """ Represents a bounding box """
    
    def __init__(self,bbox):
        """ Constructor
        bbox: {
                min_lat: float
                min_lon: float
                max_lat: float
                max_lon: float
                }
        """
        
        self.lon_min = bbox["min_lon"]
        self.lat_min = bbox["min_lat"]
        self.lon_max = bbox["max_lon"]
        self.lat_max = bbox["max_lat"]
        
        # WMS Compliance page 16
        if self.lon_min > self.lon_max or self.lat_min > self.lat_max:
            raise BBoxException("Bounding Box not correct.")
        
        # WMS Compliance page 16
        if self.lat_min < -90.0 or self.lat_max > 90.0:
            raise BBoxException("Incorrect Latitudes.")
        
        # WMS Compliance page 16
        if self.lon_min < -180.0 or self.lon_max > 360.0:
            raise BBoxException("Incorrect Longitudes")
        
        
    def display(self):
        print "lon_min: %d" % self.lon_min
        print "lat_min: %d" % self.lat_min
        print "lon_max: %d" % self.lon_max
        print "lat_max: %d" % self.lat_max