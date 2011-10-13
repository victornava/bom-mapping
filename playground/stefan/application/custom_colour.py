import numpy as np
import matplotlib as mpl

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import addcyclic
from mpl_toolkits.basemap import interp
#from scipy.interpolate import interpolate

import modules.plotting.datasource as ds
from modules.plotting.commons import BBox

#########################################################
bbox= { "min_lon" : "0" , \
        "max_lon" : "360" ,\
        "min_lat" : "-90" ,\
        "max_lat" : "90"}
url = "http://localhost:8001/atmos_latest.nc"
var = "hr24_prcp"

crange= (-4,4)
ncolors = 5
c_map = "jet"
#########################################################
cmap = mpl.cm.get_cmap(c_map)
b = BBox(bbox)
dset = ds.NetCDFDatasource(url,b,var)

fig = Figure()
canvas = FigureCanvas(fig)

ax = fig.add_axes( (0,0,1,1), \
                        frame_on = False, \
                        axis_bgcolor = 'k', \
                        alpha = 0)
                        
m = Basemap( projection = 'cyl', \
            resolution = 'c' , \
            llcrnrlon = b.lon_min, \
            llcrnrlat = b.lat_min, \
            urcrnrlon = b.lon_max, \
            urcrnrlat = b.lat_max, \
            suppress_ticks = True, \
            fix_aspect = False, \
            ax = ax)
            
# From ContourPlot
lats = dset.get_lats()
data = dset.get_data()

data,lonwrap = addcyclic(dset.get_data(), dset.get_lons())
increment = float(crange[1] - crange[0]) / float(ncolors-2)
cbounds = list(np.arange(crange[0],crange[1] + increment, increment ))

colvs = [-999]+cbounds+[999]
        
# Sort latitudes and data
lat_idx = np.argsort(lats)
lats = lats[lat_idx]
data = data[lat_idx]
        
data_lon_min = min(lonwrap)
data_lon_max = max(lonwrap)
data_lat_min = min(lats)
data_lat_max = max(lats)
        
new_lons = np.arange(data_lon_min - 1.0, data_lon_max + 1.0, 1.0)
new_lats = np.arange(data_lat_min - 1.0, data_lat_max + 1.0, 1.0)
        
x,y = m(*np.meshgrid(new_lons[:], new_lats[:]))

data_bl = interp(data,lonwrap[:],lats[:],x,y,order=1)
data_nn = interp(data,lonwrap[:],lats[:],x,y,order=0)
        
data_bl[data_nn.mask == 1] = data_nn[data_nn.mask == 1]
#m.contourf(x,y,data_bl[:,:],cbounds,cmap=cmap,extend='both')
print cbounds
col = ('g', '#FFFF33','k','#330066','#6633FF')
m.contourf(x,y,data_bl[:,:],levels=cbounds,colors=col, extend = 'both' )
m.contour(x,y,data_bl,cbounds,colors='k')
            
m.drawcoastlines()
fig.savefig("color.png", format="png")