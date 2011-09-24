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
import util.exceptions as ex

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
    pc = PlottingController(parameters)
    return pc.get_legend()

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
        #FIXME: Build argument list dynamically
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
       
        #FIXME: Fix masking .. will be shifted to datasource
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
        
        This will return an image
        """
        available_styles = {'contour' : pt.ContourPlot, \
                            'grid' : pt.GriddedPlot, \
                            'grid_treshold' : pt.GriddedTresholdPlot}
        
        key = self.parameters["styles"][0]
        
        if not available_styles.has_key(key):
            raise ex.OperationNotSupportedError(key)
        
        PlottingController.__create_contours(self,available_styles[key])
        
      #  self.m.drawcoastlines()
        return PlottingController.__create_image(self)
    
    
    def get_legend(self):
        """
        Responsible for wrapping the GetLegend request
        
        This will return an image.
        """
        
        #FIXME: Ugly ... replace without having to print map first
        PlottingController.__create_contours(self,pt.GriddedPlot)
        
        DPI = 100.0
        font_size = 8
        self.fig = Figure(figsize=(64/DPI,256/DPI))
        self.canvas = FigureCanvas(self.fig)
        #self.fig.set_figwidth(64/DPI)
        #self.fig.set_figheight(256/DPI)
        
        ax = self.fig.add_axes([0,0.1,0.2,0.8],axis_bgcolor = 'k')
        
        cbar = self.fig.colorbar(self.main_render, \
                                 cax=ax, \
                                 extend='both', \
                                 format='%1.1f' \
                                 )
                                 
        #FIXME: need additional datasource method
        cbar.set_label('Saurabh i need an extra method in ds!!', \
                        fontsize=font_size)
       
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(font_size)
            
        return PlottingController.__create_image(self)
    
    
    def get_full_figure(self):
        pass
    
    
    
    def __create_image(self):
        """ Create image with the given format an returns it. If iamge type is
        not supported, an exception is raised:
        """
        supported_formats = [ 'png', 'svg' ]
        img_format = self.parameters["format"]
        
        if not img_format in supported_formats:
            raise ex.InvalidFormatError(img_format)
       
        img_data = StringIO.StringIO()
        self.fig.savefig(img_data,format=img_format,transparent=True)
        
        value = img_data.getvalue()
        img_data.close()
        
        return value
    
    def __create_contours(self,style_type):
        """
        This class does the actual work, but does not create images. Only
        manipulates the Basemap object.
        
        style_type: The class we have to create
        """

        plot = style_type(self.parameters, \
                          self.m, \
                          self.lon, \
                          self.lat, \
                          self.var)
        
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
       