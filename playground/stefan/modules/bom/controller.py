"""
This class contains the controller class for the various types of maps
generated
"""

from bom.map.MapGenerator import MapGenerator

class Controller(object):
    """
    This class is the glue between our models
    """
    
    OVERLAY_CONTOUR = 0
    OVERLAY_GRID = 1
    OVERLAY_GRID_TRESHHOLD = 2
    
    def __init__(self,bbox):
        self.bbox = bbox
        
    
    def getMap(self):
        """ This method returns a map for the specified bounding box
        """
        #TODO: implement
        pass
    
    def getOverlay(self):
        """ This method returns an overlay for the specified bounding box
        and data source.
        
        Supported Overlays:
            - Contour
            - Grid
            - Grid Threshold
        """
        #TODO: implement
        pass
    
    def getLegend(self):
        """ This method returns the legend 
        """
        pass