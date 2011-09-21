"""
This module contains classes for the various plot types that are supported.

The following types are supported:

    - contour
    - grid
    - grid_treshhold
"""

# Interface
from abc import ABCMeta
from abc import abstractmethod

class IPlotType(object):
    """ Interface for creating different plotting types. Subclass this if
    you want to add a new plotting style.
    
    parameters: dictionary of parameters defined in plotting_controller.py
    m: Basemap instance to draw on
    lons: numpy array of longitudes
    lats: numpy array of latitudes
    data: numpy aray of data
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self,parameters,m,lons,lats,data):
        self.parameters = parameters
        self.m = m
        self.lons = lons
        self.lats = lats
        self.data = data
   
    @abstractmethod
    def plot(self):
        """ Executes and plots the appropriate plot """
        
        # minimum self preparation
        self.data, lonwrap = addcyclic(self.data, self.lons)
        self.x, self.y = self.m( *np.meshgrid(lonwrap[:],self.lats[:]) )
        
       
       
       
# Implementations

from mpl_toolkits.basemap import addcyclic
import numpy as np
import matplotlib as mpl

class GriddedPlot(IPlotType):
    """
    Class responsible for creating gridded plots
    """
    
    def __init__(self,parameters,m,lons,lats,data):
        IPlotType.__init__(self,parameters,m,lons,lats,data)

        
    def plot(self):
        IPlotType.plot(self)
        
        colormap = mpl.cm.get_cmap(self.parameters["palette"])
        crange = self.parameters["color_range"]
        
        self.main_render = self.m.pcolormesh(self.x, \
                                             self.y, \
                                             self.data[:,:], \
                                             vmin=crange[0], \
                                             vmax=crange[1], \
                                             cmap=colormap)
        