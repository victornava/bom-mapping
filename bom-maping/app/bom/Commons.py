"""
This class should contain the common datatypes that are needed to transfer data
from the WMS to the Plotting module
"""

class PlottingParams(object):
    
    def __init__(self):
        """ Constructor """
        pass
    
    
class BBox(object):
    """ Bounding Box
    
    This Class represents a Bounding Box with min and max lon/lat
    
    TODO: Add validation
    """
    def __init__(self,minX,minY,maxX,maxY):
        """ Constructor """
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY