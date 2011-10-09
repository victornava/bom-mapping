""" Plotting Controller

All functionality that has to do with plotting goes into this module.
The Parameter passed to the functions is a dictionary which can have the 
following keys and values:

dictionary: { key:value, ...}
list: []
tuple: ()

  parameters:
        bbox:   {
                min_lat: string
                min_lon: string
                max_lat: string
                max_lon: string
                }
        width : string
        height : string
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
        color_scale_range: [ string, string, ...]
        n_colors: [ string, ...]
        palette: string
        
Author: Stefan Fuchs (s3260968@student.rmit.edu.au)
"""
import numpy as np
import modules.plotting.plot_type as pt
import modules.plotting.datasource as ds
import matplotlib as mpl
import datetime
import StringIO
import util.exceptions as ex

from modules.plotting.commons import BBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import addcyclic
from mpl_toolkits.basemap import num2date


# def get_contour(parameters):
#     """ Returns a contour plot for the specified parameters """
#     pc = PlottingController(parameters)
#     return pc.get_contour()
    
# FIXME should accept defaults as argument and return: content, format
def get_contour(parameters, defaults):
    """ Returns a contour plot for the specified parameters """
    pc = PlottingController(parameters)
    return pc.get_contour(), 'png'    
    
# FIXME should accept defaults as argument and return: content, format
def get_legend(parameters):
    """ Returns the scale only"""
    pc = PlottingController(parameters)
    return pc.get_legend()

# FIXME should accept defaults as argument and return: content, format
def get_full_figure(parameters):
    """ Returns a downloadable version and combines the contour plot, legend,
    a description for the plot overlayed with coastlines. """
    pc = PlottingController(parameters)
    return pc.get_full_figure()

    
class PlottingController(object):
    """ Plotting Controller 
    
    This class controlls all the plotting related functionality.
    """
    
    def __init__(self,parameters):
        """ Constructor """
        v = ParameterValidator(parameters)
        self.parameters = v.validate()
        self.DPI = 100.0
       
        self.bbox = BBox(parameters["bbox"])

        # 1. Retrieve the data
        self.dset = self.__evaluate_datasource_type() (
                                self.parameters["source_url"], \
                                self.bbox, \
                                self.parameters["layers"][0], \
                                self.parameters["time"], \
                                self.parameters["time_index"], \
                                True
                                )
        self.lat = self.dset.get_lats()
        self.lon = self.dset.get_lons()
        self.var = self.dset.get_data()
      
            # 1.1 Normalise data
        self.bbox,self.lon,self.var = \
                self.__transform_lons(self.bbox, \
                                      self.lon, \
                                      self.var)
      
        # 2. Set up figure
        self.bmapuclon = self.bbox.lon_max
        self.bmaplclon = self.bbox.lon_min
        self.bmapuclat = min(90, self.bbox.lat_max)
        self.bmaplclat = max(-90, self.bbox.lat_min)
        
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
      
        # 3. Set up basemap
        ax = self.fig.add_axes( (0,0,1,1), \
                                frame_on = False, \
                                axis_bgcolor = 'k', \
                                alpha = 0 , \
                                visible = False )
                                
        self.m = Basemap( projection = 'cyl', \
                          resolution = 'c' , \
                          llcrnrlon = self.bmaplclon, \
                          llcrnrlat = self.bmaplclat, \
                          urcrnrlon = self.bmapuclon, \
                          urcrnrlat = self.bmapuclat, \
                          suppress_ticks = True, \
                          fix_aspect = False, \
                          ax = ax)
                         
                         
    def get_legend(self):
        """
        Responsible for wrapping the GetLegend request
        
        Returns an image.
        """
        
        #FIXME: Ugly ... replace without having to print map first
        ax = self.fig.add_axes( (0,0,1,1), \
                                frame_on = False, \
                                axis_bgcolor = 'k')
        self.m.ax = ax
        self.__create_contours(pt.GriddedPlot)
      
        self.fig = Figure(figsize=(64/self.DPI,256/self.DPI))
        self.canvas = FigureCanvas(self.fig)
        
        self.__create_legend((0,0.1,0.2,0.8))
            
        return self.__create_image()
    
    
    def get_contour(self):
        """ Responsible for wrapping the GetMap request.
        
        Returns an image.
        """
        # Calculate offsets for stuff
        bmaplatmin, bmaplonmin = self.m(self.bbox.lat_min, self.bbox.lon_min)
        bmaplatmax, bmaplonmax = self.m(self.bbox.lat_max, self.bbox.lon_max)
        
        print bmaplatmin, bmaplonmin
        print bmaplatmax, bmaplonmax
        
        lon_offset1 = abs(self.bmaplclon - bmaplonmin)
        lat_offset1 = abs(self.bmaplclat - bmaplatmin)
        #lon_offset2 = abs(self.bmapuclon - bmaplonmax)
        #lat_offset2 = abs(self.bmapuclat - bmaplatmax)
        
        lon_normstart = lon_offset1 / abs(bmaplonmax - bmaplonmin)
        lat_normstart = lat_offset1 / abs(bmaplatmax - bmaplatmin)
        
        ax_xfrac = abs( self.bmapuclon - self.bmaplclon ) / \
                   abs( bmaplonmax - bmaplonmin )
                   
        ax_yfrac = abs( self.bmapuclat - self.bmaplclat ) / \
                   abs( bmaplatmax - bmaplatmin)
        
        coords = (lon_normstart, lat_normstart, ax_xfrac, ax_yfrac)
        
        #####
        ax = self.fig.add_axes( coords, \
                                frame_on = False, \
                                axis_bgcolor = 'k')
        self.m.ax = ax
        self.__create_contours(self.__evaluate_plot_type())
        return self.__create_image()
    
    
    def get_full_figure(self, n_merid = 5, n_para = 5):
        """ Responsibe for wrapping the GetFullFigure request.
        
        Returns an image.
        
        n_merid: Number of meridians we want to print as an overlay
        n_para: number of parallels we want printed as an overlay
        """
        tick_font_size = 8
        title_font_size = 9
        
        plot_dims = self.__calc_plot_dims()
        ax = self.fig.add_axes( plot_dims, \
                                frame_on = False, \
                                axis_bgcolor = 'k')
        
        self.m.ax = ax
        self.__create_contours(self.__evaluate_plot_type())
        self.__create_legend((0.8,0.1,0.02,plot_dims[3]))
        
        # Creating the overlay
        base = (self.bbox.lon_max - self.bbox.lon_min)/float(n_merid)
        meridians = [ self.bbox.lon_min + i*base for i in range(n_merid)]
        
        base = (self.bbox.lat_max - self.bbox.lat_min)/float(n_para)
        parallels = [ self.bbox.lat_min + i*base for i in range(1,n_para+1)]
        
        self.m.drawcoastlines()
        self.m.drawmeridians(meridians, \
                             labels = [0,1,0,1], \
                             fmt = "%3.1f", \
                             fontsize = tick_font_size)
        self.m.drawparallels(parallels, \
                             labels= [1,0,0,0], \
                             fmt = "%3.1f", \
                             fontsize = tick_font_size)
        self.m.drawparallels([0], \
                             linewidth = 1, \
                             dashes = [1,0], \
                             labels = [0,1,1,1], \
                             fontsize = tick_font_size)
        
        self.fig.text(0.05,0.98,self.__get_plot_title(), \
                      va='top', fontsize=title_font_size)
        
        return self.__create_image(transparent=False)
    
    
    def __create_image(self,transparent=True):
        """ Create image with the given format an returns it. If iamge type is
        not supported, an exception is raised:
        
        transparent: True/False for transparent background
        """
       
        supported_formats = [ 'png', 'svg' ]
        img_format = self.parameters["format"]
        
        if not img_format in supported_formats:
            raise ex.InvalidFormatError(img_format)
       
        img_data = StringIO.StringIO()
       
        self.fig.savefig(img_data, \
                         format = img_format, \
                         transparent=transparent)
        
        value = img_data.getvalue()
        img_data.close()
        
        return value
    
    def __create_contours(self,style_type):
        """
        This class does the actual work, but does not create images. Only
        manipulates the Basemap object.
        
        style_type: The class we have to create
        """
        
        # Set size of the image
        self.fig.set_dpi(self.DPI)
        self.fig.set_size_inches(self.parameters["width"]/self.DPI, \
                                 self.parameters["height"]/self.DPI)
                                 
        plot = style_type(self.parameters, \
                          self.m, \
                          self.lon, \
                          self.lat, \
                          self.var)
        
        self.main_render = plot.plot()

        
    def __create_legend(self,coords):
        """ Creates the legend graphic at the the specified coords
        
        coords: rect for the axes
        """
        ax = self.fig.add_axes(coords,axis_bgcolor = 'k')
        
        cbar = self.fig.colorbar(self.main_render, \
                                 cax=ax, \
                                 extend='both', \
                                 format='%1.1f' \
                                 )
                                
        font_size = 8
        cbar.set_label( self.dset.get_var_unit(), \
                        fontsize=font_size)
       
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(font_size)
        
    
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
       
       
    def __calc_plot_dims(self , \
                        max_xfrac = 0.7, \
                        max_yfrac = 0.7, \
                        desired_ratio = 1.0):
        """ Calculate apropriate plotting dimensions for the full figure
        image.
        """
        height = self.parameters["height"]
        width = self.parameters["width"]
        max_height = max_yfrac * height
        max_width = max_xfrac * width
        
        nlat = float(self.bbox.lat_max - self.bbox.lat_min)
        nlon = float(self.bbox.lon_max - self.bbox.lon_min)
        
        plot_aspect_ratio = max_width / max_height
        lat_lon_aspect_ratio = (nlon/nlat) * plot_aspect_ratio
        
        if lat_lon_aspect_ratio > desired_ratio:
            # Image needs to be narrower
            xfrac = desired_ratio * (nlon/nlat) * max_yfrac * \
                    (float(width)/height)
            yfrac = max_yfrac
        else:
            #Image needs to be shorter
            yfrac = (1./desired_ratio) * (nlat/nlon) * max_xfrac * \
                    (float(width)/height)
            xfrac = max_xfrac
        
        # Ensure we are within bounds
        if yfrac > max_yfrac:
            xfrac = xfrac * max_yfrac/yfrac
            yfrac = max_yfrac
            
        if xfrac > max_xfrac:
            yfrac = yfrac * max_xfrac/xfrac
            xfrac = max_xfrac
        
        #print lat_lon_aspect_ratio
        #print "xfrac: %f" % xfrac
        #print "yfrac: %f" % yfrac
        return (0.08,0.08,xfrac,yfrac)
        
        
    def __get_plot_title(self):
        """" Returns the title for the full figure request"""
        header = "PASAP: Dynamical Seasonal Outlooks for the Pacific."
        subheader1 = "Outlook based on POAMA 1.5 CGCM adjusted for "\
                     "historical skill"
        subheader2 = "Experimental outlook for demonstration and research only"
        
        start_date = datetime.datetime.strftime( \
                            num2date( self.dset.get_init_date()[0], \
                                      self.dset.get_time_units()), \
                                      "%Y%m%d")
        
        title = header + '\n' + \
                subheader1 + '\n' + \
                subheader2 + '\n' + \
                'Variable: ' + self.parameters['layers'][0] + \
                ' (' + self.dset.get_var_unit() + ')\n' + \
                'Model initlialised ' + start_date + '\n' + \
                'Forecast period: ' + str(self.dset.get_time_label())

        return title
        
        
    def __evaluate_plot_type(self):
        """ Evaluates the correct class for the type of plot. 
        
        Throws an exception, if the requested type is not available.
        """
        
        # Add to available_styles list if there are new types of plots
        available_styles = {'contour' : pt.ContourPlot, \
                            'grid' : pt.GriddedPlot, \
                            'grid_treshold' : pt.GriddedTresholdPlot}
        
        key = self.parameters["styles"][0]
        
        if not available_styles.has_key(key):
            raise ex.StyleNotDefinedError(key)
        
        return available_styles[key]
        
        
    def __evaluate_datasource_type(self):
        """ Evaluates what type of data source needs to be created based on
            the file extension of the url """
        
        available_sources = { '.nc' : ds.NetCDFDatasource }
        
        key = None
        for k in available_sources.keys():
            if self.parameters["source_url"].endswith(k):
                key = k
                break;
        
        if key == None:
            raise ex.DatasourceNotSupportedError("Unsupported Datasource")
        
        return available_sources[key]
        
class ParameterValidator(object):
    """ Class responsible for validating parameters passed to the controller
    """
    
    def __init__(self,parameters):
        self.parameters = parameters
        
        
    def validate(self):
        """ Validates the passed parameters and returns the dictionary with
        changed values were necessary.
        """
        # 1. Validate that all mandatory arguments are supplied
        self.__check_mandatory_parameters(self.parameters)
        
        # 2. Check that values that are not supplied have sane defaults
        self.__check_defaults(self.parameters)
        
        # 3. Check that numerical values are really numerical
        self.__check_numericals(self.parameters)
        
        return self.parameters
        
        
    def __check_numericals(self,parameters):
        """ Validates that numerical values are numerical """
        # dictionary with names and types
        check = { "width" : int, \
                  "height" : int }
        for k in check:
            self.__check_single_value(parameters,k,check[k],True)
            
        #TODO: Add values where negative doesnt matter
        
        # check for values that need to be in a list
        check = { "color_scale_range" : int , \
                  "n_colors" : int }
        for k in check:
            self.__check_list_value(parameters,k,check[k])
        
        
    def __check_single_value(self,parameters,name,dtype,neg_check = False):
        """ Checks a single value for the given type
        
        parameters: dictionary with parameters
        name: name of the parameters
        dtype: data type to be converted to
        neg_check: Set to True if values have to be 1 or bigger
        """
        try:
            parameters[name] = dtype(parameters[name])
        except:
            raise ex.InvalidParameterValueError( name + '(' + \
                                                 str(parameters[name]) + ')')
                                                 
        if neg_check and parameters[name] < 1:
            raise ex.InvalidParameterValueError( name + '(' + \
                                                 str(parameters[name]) + ')')
            
    
    
    def __check_list_value(self,parameters,name,dtype):
        """ Check for values that need to be in a list 
        
        parameters: dictionary with parameters
        name: name of the parameters
        dtype: data type to be converted to
        """
       
        try:
            parameters[name] = list([dtype(a) for a in parameters[name]])
        except:
            raise ex.InvalidParameterValueError( name + '(' + \
                                                 ', '.join(parameters[name]) \
                                                 + ')')
        
    
    def __check_defaults(self,parameters):
        """ Check that not supplied optional arguments have sane defaults """
        
        # dictionary for default values
        defaults = { "time_index" : "Default" ,\
                     "time" : "Default" ,\
                     "palette" : "jet" }
        
        for key in defaults.keys():
            if not parameters.has_key(key):
                parameters[key] = defaults[key]

    
    def __check_mandatory_parameters(self,parameters):
        """ Checks for mandatory parameters 
        
        This method checks if the parameters declared as mandatory were
        provided by the calling entity.
        """
        mandatory_parameters = [ "bbox" , "styles", "layers", "width", \
                                 "height", "source_url", "format" , "crs", \
                                 "color_scale_range", "n_colors" ]
        for key in mandatory_parameters:
            if not parameters.has_key(key):
                raise ex.MissingParameterError(key)