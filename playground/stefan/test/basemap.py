#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Figure setup
fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_axes((0, 0, 1, 1),frameon=True)
#fig.set_size_inches((8/m.aspect, 8.))

# Basemap
m = Basemap(llcrnrlon=0, \
            llcrnrlat=-90, \
            urcrnrlon=360, \
            urcrnrlat=90, \
            resolution= 'l', \
            projection = 'cyl', \
            lon_0 = 4.9, \
            lat_0 = 45.1, \
            suppress_ticks= True, \
            ax = ax)
            



# data
lats = [41.38, 43.18, 48.87, 43.60, 46.52, 43.28, 46.20]
lons = [ 2.18,  3.00,  2.32,  1.43,  6.63,  5.37,  6.15]
name = ['Barcelona', 'Narbonne', 'Paris', 'Toulouse', 'Lausanne', 'Marseille', 'Geneva']

#draw and save
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.fillcontinents(color='beige')
x, y = m(lons, lats)
m.plot(x, y, 'bo')
canvas.print_figure('map.png', dpi=100)