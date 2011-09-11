"""
This file contains a few helper methods
"""

class Bbox(object):
    """ Object representing a bounding box.
    
    Normalisation for a region of longitudes between 0 and 360 deg
    
    Stores variables as:
        lon_min
        lat_min
        lon_max
        lat_max
    """
    
    def __init__(self,bbox):
        """ Constructor

        bbox - tuple: ((lonMin,latMin),(lonMax,latMax))
        """

        self.lon_min, self.lon_max = check_longitudes(bbox[0][0],bbox[1][0])
        self.lat_min, self.lat_max = check_latitudes(bbox[0][1],bbox[1][1])


def check_latitudes(lat_min,lat_max):
    """ This functions ensures that latitudes are between -90 and 90
    
    lat_min: deg South latitudes (-)
    lat_max: deg North latitudes (+)
    
    returns: normalized lat_min and lat_max
    """
    l_min = max(-90,lat_min)
    l_max = min(90,lat_max)
    
    #We don't want an upside down world
    if l_min > l_max:
        l_min, l_max = l_max, l_min
        
    #TODO: what if l_min == l_max
    
    return l_min, l_max


def check_longitudes(lon_min, lon_max):
    """ This functions ensures that the minimum latitude is always smaller
        than the macheck_latitudesximum latitude, and that they are no more than 360 deg
        apart
    """
    
    l_min = lon_min % 360
    l_max = lon_max % 360
    
    if l_max <= l_min:
        l_max += 360

    return l_min, l_max