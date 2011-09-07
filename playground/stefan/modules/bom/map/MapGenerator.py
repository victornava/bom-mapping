#
# Author: Stefan Fuchs (s3260968@student.rmit.edu.au)
#

from bom.globals import bom_config as bc
import bom.utils.bom_utils as bu
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


class MapGenerator(object):
    """ Class for generating Basemap maps
    
    This class generates Basemap maps and deals with mapping latitudes and
    longitudes to the appropriate basemap coordinates
    """

    def __init__(self,bbox):
        """ Constructor

        bbox - a bom.utils.Bbox object
        """
        
        self.m = Basemap( projection='cyl', llcrnrlon=bbox.lon_min, 
                          llcrnrlat=bbox.lat_min, urcrnrlon=bbox.lon_max,
                          urcrnrlat=bbox.lat_max)
        meridians = self.__calc_lines(bbox.lon_min,bbox.lon_max,
                                      bc.NUM_MERIDIANS)
        parallels = self.__calc_lines(bbox.lat_min,bbox.lat_max,
                                      bc.NUM_PARALLELS)

        self.m.drawcoastlines()
        self.m.drawmeridians(meridians,labels=[0,1,0,1],fmt='%3.1f',
                             fontsize=bc.THICK_FONT_SIZE)
        self.m.drawparallels(parallels,labels=[1,0,0,0],fmt='%3.1f',
                             fontsize=bc.THICK_FONT_SIZE)
        self.m.drawparallels([0],linewidth=1,dashes=[1,0],labels=[0,1,1,1],
                             fontsize=bc.THICK_FONT_SIZE)

        plt.savefig("/home/fixl/bom.png")
        

    def __calc_lines(self,min_line,max_line,num_line):
        """ Calculates sensible values for longitudes and latitudes
        
        min_line - min of longitude or latitude
        max_line - max of longitude or latitude
        num_line - number of lines we want
        
        returns - an array lines(longitudes or latitudes) 
        """
        
        # Make the lines not appear on the axis
        base = (max_line - min_line)/float(num_line + 1)
        lines = [int(min_line + i*base) for i in range(1, num_line + 1)]
        
        return lines