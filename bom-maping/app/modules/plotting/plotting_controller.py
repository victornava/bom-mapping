""" Plotting Controller

All functionality that has to do with plotting goes into this module.
The Parameter passed to the functions is a dictionary which can have the 
following keys and values:

dictionary: { key:value, ...}
list: []
tuple: ()

  parameters:

        bbox:   {
                min_lat: float
                min_lon: float
                max_lat: float
                max_lon: float
                }
        width : int
        height : int
        layers : [string, ...]
        styles : [string, ...]
        crs:    {
                name: string
                identifier: string
                }
        format: string
        time: string
        time_index: string
        source_url: string
        color_scale_range: [int,int] min,max
        n_color: int
        palette: string
"""
import numpy as np
import modules.plotting.plot_type as pt
import modules.plotting.datasource as ds
import matplotlib as mpl
import StringIO

from modules.plotting.commons import BBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import addcyclic


def get_contour(parameters):
    """ Returns a contour plot for the specified parameters """
    pc = PlottingController(parameters)
    return pc.get_contour()
    
    
def get_legend(parameters):
    """ Returns the scale only"""
    pass

def get_full_figure(parameters):
    """ Returns a downloadable version and combines the contour plot, legend,
    a description for the plot overlayed with coastlines. """
    pass

class PlottingController(object):
    """ Plotting Controller 
    
    This class controllsall the plotting related functionality.
    """
    
    def __init__(self,parameters):
        """ Constructor """
        
        self.parameters = parameters
        bbox = BBox(parameters["bbox"])

        # 1. Retrieve the data
        dset = ds.NetCDFDatasource( self.parameters["source_url"], \
                                    bbox, \
                                    self.parameters["layers"][0], \
                                    self.parameters["time"], \
                                    self.parameters["time_index"], \
                                    )
        #dset = open_url(self.parameters["source_url"])
        lat = dset.get_lats()
        lon = dset.get_lons()
        var = dset.get_data()
       
        #TODO: Fix masking .. will be shifted to datasource
        varm = np.ma.masked_array(var, mask=np.isinf(var))
        
            # 1.1 Normalise data
        self.bbox,lon,var = \
                    PlottingController.__transform_lons(self,bbox,lon,varm)
       
        # 2. Set up figure
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        
        # 3. Set up basemap
        self.m = Basemap( projection = 'cyl', \
                          resolution = 'c' , \
                          llcrnrlon = self.bbox.lon_min, \
                          llcrnrlat = self.bbox.lat_min, \
                          urcrnrlon = self.bbox.lon_max, \
                          urcrnrlat = self.bbox.lat_max, \
                          suppress_ticks = True, \
                          fix_aspect = False)
                          
        # 4. add data
        ax = self.fig.add_axes( (0,0,1,1), \
                                frame_on = False, \
                                axis_bgcolor = 'k')
                                
        self.m.ax = ax
        
        #  "export" important variables
        self.lat = lat
        self.lon = lon
        self.var = var

        
   
    def get_contour(self):
        """
        Responsible for wrapping the GetMap request.
        
        This will return the whole image
        """
        PlottingController.__create_contours(self)
        return PlottingController.__create_image(self)
    
    
    def get_legend(self):
        pass
    
    
    def get_full_figure(self):
        pass
    
    
    
    def __create_image(self):
        """ Create image with the given format an returns it. If iamge type is
        not supported, an exception is raised:
        """
        img_data = StringIO.StringIO()
        if self.parameters["format"] == 'png':
            self.fig.savefig(img_data,format='png',transparent=True)
        else:
            print "%s not supported!"
            #TODO: Raise Exception
    
        value = img_data.getvalue()
        img_data.close()
        
        return value
    
    def __create_contours(self):
        """
        This class does the actual work, but does not create images. Only
        manipulates the Basemap object.
        """

        #TODO: Very ugly! Maybe use state pattern here, or factory ...
        style = self.parameters["styles"][0]
        
        if style == "grid":
            plot = pt.GriddedPlot( self.parameters, \
                                   self.m, \
                                   self.lon, \
                                   self.lat, \
                                   self.var)
            print "grid style selected"
        elif style == "grid_treshold":
            plot = pt.GriddedTresholdPlot( self.parameters, \
                                           self.m, \
                                           self.lon, \
                                           self.lat, \
                                           self.var)
            print "grid_treshhold selected"
        elif style == "contour":
            plot = pt.ContourPlot( self.parameters, \
                                   self.m, \
                                   self.lon, \
                                   self.lat, \
                                   self.var)
            print "contour style selected"
        else:
            print "%s no supported .. raise exception" % style
            #TODO: raise exception
        
        self.main_render = plot.plot()

    
    def __transform_lons(self,bbox,lons,var):
        """ Take Bounding box longitudes and transform them for sensible
        Basemap plotting.
        
        bbox: Bounding Box ... values will change in there
        lons: numpy array of longitudes
        var: numpy array of field to be plotted
        """
        
        to_360 = lambda x: ( x % 360. )
        
        # Put everything into a range greater 0 right away
        lon_min = to_360(bbox.lon_min)
        lon_max = to_360(bbox.lon_max)
        lons = to_360(lons)
        
        # If lon_min is greater than lon_max after transformation
        if lon_min > lon_max:
            lon_max += 360.
        
        # If both are the same i.e. 360 degree print
        if lon_min == lon_max:
            lon_max += 360.
        
        # If lon_max greater than 360, remap longitudes to that range
        if lon_max > 360.:
            idx = lons < lon_min
            lons[idx] = lons[idx] + 360.
        
        bbox.lon_min = lon_min
        bbox.lon_max = lon_max
        
        # Ensure longitudes are ascending, and shuffle field with same indices
        idx = np.argsort(lons)
        lons = lons[idx]
        var = var[:,idx]
        var, lons = addcyclic(var,lons)
        
        return bbox,lons,var
       