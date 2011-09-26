"""
This module contains classes for the various plot types that are supported.

The following types are supported:

    - contour
    - grid
    - grid_treshold
"""

# Interface
from abc import ABCMeta
from abc import abstractmethod

# Imports for implementations
import numpy as np
import matplotlib as mpl

from mpl_toolkits.basemap import addcyclic
from mpl_toolkits.basemap import interp
from scipy.interpolate import interpolate

class IPlotType(object):
    """ Interface for creating different plotting types. Subclass this if
    you want to add a new plotting style.
    """

    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self,parameters,m,lons,lats,data):
        """ Constructor
        
        parameters: dictionary of parameters defined in
        plotting_controller.py
        m: Basemap instance to draw on
        lons: numpy array of longitudes
        lats: numpy array of latitudes
        data: numpy aray of data
        """
        
        self.parameters = parameters
        self.m = m
        self.lons = lons
        self.lats = lats
        self.data = data
        
        self.ncolors = self.parameters["n_color"]
        self.cmap = self.__cmap_discretise( mpl.cm.get_cmap( \
                                                self.parameters["palette"]),\
                                            self.ncolors)
   
    @abstractmethod
    def plot(self):
        """ Executes and plots the appropriate plot """
        
        # minimum self preparation
        self.data, lonwrap = addcyclic(self.data, self.lons)
        self.x, self.y = self.m( *np.meshgrid(lonwrap[:],self.lats[:]) )
       
       
    def __cmap_discretise(self,cmap, N):
        """ Returns a discrete colormap from a continuous colormap 
        
            cmap: colormap instance, e.g. cm.jet
            N: Number of colors
            
            http://www.scipy.org/Cookbook/Matplotlib/ColormapTransformations
        """
        cdict = cmap._segmentdata.copy()
        # N colors
        colors_i = np.linspace(0,1.,N)
        # N + 1 indices
        indices = np.linspace(0,1.,N+1)
        
        for key in ('red','green','blue'):
            # Find the N colors
            D = np.array(cdict[key])
            I = interpolate.interp1d(D[:,0], D[:,1])
            colors = I(colors_i)
            #Place those colors at the correct indices
            A = np.zeros((N+1,3),float)
            A[:,0] = indices
            A[1:,1] = colors
            A[:-1,2] = colors
            #Create a tuple for the dictionary
            L = []
            for l in A:
                L.append(tuple(l))
            cdict[key] = tuple(L)
        
        return mpl.colors.LinearSegmentedColormap('colormap',cdict,1024)
       
       
# Implementations


class GriddedPlot(IPlotType):
    """
    Class responsible for creating gridded plots
    """
    
    def __init__(self,parameters,m,lons,lats,data):
        """ Constructor """
        IPlotType.__init__(self,parameters,m,lons,lats,data)

        
    def plot(self):
        IPlotType.plot(self)
        
        #colormap = mpl.cm.get_cmap(self.parameters["palette"])
        crange = self.parameters["color_range"]
        
        self.main_render = self.m.pcolormesh(self.x, \
                                             self.y, \
                                             self.data[:,:], \
                                             vmin=crange[0], \
                                             vmax=crange[1], \
                                             cmap=self.cmap)
                                             
        return self.main_render
        
    
class GriddedTresholdPlot(IPlotType):
    """
    Class responsible for creating gridded treshold plots
    """
    
    def __init__(self,parameters,m,lons,lats,data):
        """ Constructor """
        IPlotType.__init__(self,parameters,m,lons,lats,data)
    
    
    def plot(self):
        IPlotType.plot(self)
        
        #cmap = mpl.cm.get_cmap(self.parameters["palette"])
        crange = self.parameters["color_range"]
        #ncolors = self.parameters["n_color"]
        
        increment = float(crange[1] - crange[0]) / float(self.ncolors)
        cbounds = list(np.arange(crange[0],crange[1] + increment, increment ))
        
        cnorm = mpl.colors.BoundaryNorm(cbounds,self.cmap.N)
        self.main_render = self.m.pcolor( self.x, \
                                          self.y, \
                                          self.data[:,:], \
                                          vmin=crange[0], \
                                          vmax=crange[1], \
                                          cmap=self.cmap, \
                                          norm=cnorm)
        
        return self.main_render
        
class ContourPlot(IPlotType):
    """
    Class responsible for creating contour plots
    """
    
    def __init__(self,parameters,m,lons,lats,data):
        """ Constructor """
        IPlotType.__init__(self,parameters,m,lons,lats,data)
        
        
    def plot(self):
        
        #cmap = mpl.cm.get_cmap(self.parameters["palette"])
        crange = self.parameters["color_range"]
        ncolors = self.parameters["n_color"]
        
        self.data,lonwrap = addcyclic(self.data,self.lons)
        
        increment = float(crange[1] - crange[0]) / float(ncolors-2)
        cbounds = list(np.arange(crange[0],crange[1] + increment, increment ))
        # TODO: Color stuff
        
        #cmap = self.cmap_discretise(cmap,ncolors)
        
        colvs = [-999]+cbounds+[999]
        
        # Sort latitudes and data
        lat_idx = np.argsort(self.lats)
        self.lats = self.lats[lat_idx]
        self.data = self.data[lat_idx]
        
        data_lon_min = min(lonwrap)
        data_lon_max = max(lonwrap)
        data_lat_min = min(self.lats)
        data_lat_max = max(self.lats)
        
        new_lons = np.arange(data_lon_min - 1.0, data_lon_max + 1.0, 1.0)
        new_lats = np.arange(data_lat_min - 1.0, data_lat_max + 1.0, 1.0)
        
        x,y = self.m(*np.meshgrid(new_lons[:], new_lats[:]))
        
        # Two pass interpolation to deal with the mask.
        # First pass does bilinear, the next does nearest neighbour
        # interpolation.
        # It's not clear this is working, and the problem is likely
        # solved by ensuring the right mask is used!
        data_bl = interp(self.data,lonwrap[:],self.lats[:],x,y,order=1)
        data_nn = interp(self.data,lonwrap[:],self.lats[:],x,y,order=0)
        
        data_bl[data_nn.mask == 1] = data_nn[data_nn.mask == 1]
        
        self.main_render = self.m.contourf( x, \
                                            y, \
                                            data_bl[:,:], \
                                            cbounds, \
                                            cmap=self.cmap, \
                                            extend='both')
        contours = self.m.contour(x,y,data_bl,cbounds,colors='k')
        contours.clabel(colors='k',rightside_up=True,fmt='%1.1f',inline=True)
        
        return self.main_render