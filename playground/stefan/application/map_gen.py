#!/usr/bin/python

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import StringIO

def createMap(name='cyl'):
    m = Basemap(projection='cyl', llcrnrlat=-90,\
    urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='c')

    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')

#    m.drawparallels(np.arange(-90.,91.,15.))
    m.drawmeridians(np.arange(-180.,181.,30.))
    m.drawmapboundary(fill_color='aqua')
    
    plt.title("Equidistant Cylindrica Projection")
    imagedata = StringIO.StringIO()
    
    plt.savefig(imagedata,format='png')
    
    #return 'hello'
    return imagedata.getvalue()


if __name__ == '__main__':
    m = createMap('cyl')
    print m
