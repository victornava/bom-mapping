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
    def __init__(self,parameters,m,lons,lats,data, fig):
        """ Constructor
        
        parameters: dictionary of parameters defined in
        plotting_controller.py
        m: Basemap instance to draw on
        lons: numpy array of longitudes
        lats: numpy array of latitudes
        data: numpy aray of data
        fig: the figure
        """
        
        self.parameters = parameters
        self.m = m
        self.lons = lons
        self.lats = lats
        self.data = data
        self.fig = fig
        
        self.ncolors = self.parameters["n_colors"][0]
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
    
    def __init__(self,parameters,m,lons,lats,data,fig):
        """ Constructor """
        IPlotType.__init__(self,parameters,m,lons,lats,data,fig)

        
    def plot(self):
        IPlotType.plot(self)
        
        cmap = mpl.cm.get_cmap(self.parameters["palette"])
        crange = self.parameters["color_scale_range"]
        
        self.main_render = self.m.pcolormesh(self.x, \
                                             self.y, \
                                             self.data[:,:], \
                                             vmin=crange[0], \
                                             vmax=crange[1], \
#                                             cmap=self.cmap)
                                             cmap=cmap)
                                             
        return self.main_render
        
    
class GriddedTresholdPlot(IPlotType):
    """
    Class responsible for creating gridded treshold plots
    """
    
    def __init__(self,parameters,m,lons,lats,data,fig):
        """ Constructor """
        IPlotType.__init__(self,parameters,m,lons,lats,data,fig)
    
    
    def plot(self):
        IPlotType.plot(self)
        cmap = mpl.cm.get_cmap(self.parameters["palette"])
        crange = self.parameters["color_scale_range"]
        #ncolors = self.parameters["n_color"]
        
        increment = float(crange[1] - crange[0]) / float(self.ncolors)
        cbounds = list(np.arange(crange[0],crange[1] + increment, increment ))
        
#        cnorm = mpl.colors.BoundaryNorm(cbounds,self.cmap.N)
        cnorm = mpl.colors.BoundaryNorm(cbounds,cmap.N)
        self.main_render = self.m.pcolor( self.x, \
                                          self.y, \
                                          self.data[:,:], \
                                          vmin=crange[0], \
                                          vmax=crange[1], \
#                                          cmap=self.cmap, \
                                          cmap=cmap, \
                                          norm=cnorm)
        
        return self.main_render
        
class ContourPlot(IPlotType):
    """
    Class responsible for creating contour plots
    """
    
    def __init__(self,parameters,m,lons,lats,data,fig):
        """ Constructor """
        IPlotType.__init__(self,parameters,m,lons,lats,data,fig)
        
        
    def plot(self):
        
        #crange = self.parameters["color_scale_range"]
        #ncolors = self.parameters["n_colors"][0]
        
        self.data,lonwrap = addcyclic(self.data,self.lons)
        
        #increment = float(crange[1] - crange[0]) / float(ncolors-2)
        #cbounds = list(np.arange(crange[0],crange[1] + increment, increment ))
        # TODO: Color stuff
        
        #cmap = self.cmap_discretise(cmap,ncolors)
        
        #FIXME: Do we need this?
        #colvs = [-999]+cbounds+[999]
        
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
        
        if self.parameters.has_key('custom_levels'):
            self.__print_custom_color_plot(x,y,data_bl)
        else:
            self.__print_cmap_plot(x,y,data_bl)
        """
        self.main_render = self.m.contourf( x, \
                                            y, \
                                            data_bl[:,:], \
                                            cbounds, \
                                            cmap=self.cmap, \
                                            extend='none')
                                            """
        #contours = self.m.contour(x,y,data_bl,cbounds,colors='k')
        #contours.clabel(colors='k',rightside_up=True,fmt='%1.1f',inline=True)
        
        return self.main_render

        
    def __print_cmap_plot(self,x,y,data):
        """ Creates standard contour plot """
        crange = self.parameters["color_scale_range"]
        ncolors = self.parameters["n_colors"][0]
        
        increment = float(crange[1] - crange[0]) / float(ncolors-2)
        cbounds = list(np.arange(crange[0],crange[1] + increment, increment ))
        
        self.main_render = self.m.contourf( x, \
                                            y, \
                                            data[:,:], \
                                            cbounds, \
                                            cmap=self.cmap, \
                                            extend='both')
        
        contours = self.m.contour(x,y,data,cbounds,colors='k')
        contours.clabel(colors='k',rightside_up=True,fmt='%1.1f',inline=True)
        
    
    def __print_custom_color_plot(self,x,y,data):
        """ Creates contour plot with custom colors """
        extend = self.__find_extend()
        
        self.main_render = self.m.contourf( x, \
                                            y, \
                                            data[:,:], \
                                levels=self.parameters['custom_levels'], \
                                            extend=extend, \
                                            ** self.__find_correct_color())
                                            
        if self.__has_min_ext():
            self.main_render.cmap.set_under(self.parameters["custom_min"])
            
        if self.__has_max_ext():
            self.main_render.cmap.set_over(self.parameters["custom_max"])
            
        contours = self.m.contour( x, \
                                   y, \
                                   data, \
                                   levels=self.parameters['custom_levels'], \
                                   colors='k')
        

        
        contours.clabel(colors='k',rightside_up=True,fmt='%1.1f',inline=True)
        
        # FIXME: This is a workaround to display the extend properly
        ax = self.fig.add_axes((1,1,1,1), visible = False)
        self.fig.colorbar(self.main_render, ax=ax)
        
        
    def __find_extend(self):
        """ Finds out the correct extend
       
http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.
contourf
        """
        
        if self.__has_min_ext() and self.__has_max_ext():
            return 'both'
        
        if self.__has_min_ext():
            return 'min'
            
        if self.__has_max_ext():
            return 'max'
            
        return 'neither'
        
    
    def __find_correct_color(self):
        """ Returns a dictionary with the correct colors to be used.
        
        If no custom colors were specified, the supplied cmap will be used.
        """
        if self.parameters.has_key('custom_colors'):
            return { 'colors' : self.parameters['custom_colors'] }
        else:
            return { 'cmap' : self.cmap }
    
    def __has_min_ext(self):
        return self.parameters.has_key('custom_min')
        
        
    def __has_max_ext(self):
        return self.parameters.has_key('custom_max')