# from numpy  import *
# # import pydap
# from pydap.client import open_url
# prototype imports

import cgi
import cgitb
import sys
import os
import site

# import pydap
# from pydap.client import open_url

import numpy as np
from time import strftime, time, strptime
import datetime
import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap, addcyclic, date2num, num2date
from mpl_toolkits.basemap import interp
from scipy.interpolate import interpolate
import StringIO


# return the version number of a library
# def version(library):
#     import pkg_resources
#     return library + ": " +pkg_resources.get_distribution(library).version
#     
# print version("numpy")
print "All good"

