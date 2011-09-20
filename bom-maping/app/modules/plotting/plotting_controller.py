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
        color_scale_range: (int,int) min,max
        n_color: int
        palette: string
        
"""




def get_contour(parameters):
    """ Returns a contour plot for the specified parameters """
    pass

def get_legend(parameters):
    """ Returns the scale for the specified parameters """
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
        pass