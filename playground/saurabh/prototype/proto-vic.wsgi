#! python

import cgi
import cgitb
cgitb.enable()
import sys
import os
import site

# CHANGED
# Set up the pythonpath
# for path in os.environ.get('PYTHON_PATH_PASAP','').split(':'):
#     site.addsitedir(path)

# Set up a temporary directory for matplotlib    
os.environ['MPLCONFIGDIR'] = '/tmp/'

from pydap.client import open_url
# import numpy as np
from time import strftime, time, strptime
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap, addcyclic, date2num, num2date
from mpl_toolkits.basemap import interp

#STUCK can't import this library (in apache)
from scipy.interpolate import interpolate
import StringIO

# Create a cache for storing data from urls
cache = {}

def application(environ, start_response):

    start = time()

    params = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    download = params.getvalue('DOWNLOAD', False);
    
    # CHANGED
    output = doWMS(params)
    # output = "it work"
    
    print "Duration: %s" % str(time() - start)
    if output:
        if download:
            filename = "map.png"
            start_response('200 OK', [
                ('Content-Disposition', 'attachment;filename=%s' % filename),
                ('Content-Type', 'image/png'),
                ("Content-length", str(len(output))),
                ])
        else:
            start_response('200 OK', [
                # CHANGED
                ('Content-Type', 'image/png'),
                # ('Content-Type', 'text/html'),
                ("Content-length", str(len(output))),
                ])

        return [output]
    else:
        error = "<html><head><title>Sorry</title></head><body><p>" 
        error += "There was an error and the server was unable to process your request."
        error += "</p></body></html>"
        start_response('500 Internal Error', [
            ('Content-Type', 'text/html'),
            ("Content-length", str(len(error))),
            ], sys.exc_info)
        return [error,]

def doWMS(params):
    """ Provides a wrapper for the map-plot function. """
    varname = params.getvalue('LAYERS', params.getvalue('LAYER','hr24_prcp'))
    bbox = params.getvalue('BBOX','-180,-90,180,90')
    projection_code = params.getvalue('CRS', 'EPSG:4283')
    
    # CHANGED
    # url = params.getvalue('DAP_URL',
    #         'http://opendap.bom.gov.au:8080/thredds/dodsC/PASAP/atmos_latest.nc')
    
    url = "http://localhost:8001/ocean_latest.nc"
    
    imgwidth = int(params.getvalue('WIDTH',256))
    imgheight = int(params.getvalue('HEIGHT',256))
    request = params.getvalue('REQUEST', 'GetMap')
    time = params.getvalue('TIME','Default')
    palette = params.getvalue('PALETTE','jet')
    style = params.getvalue('STYLE','grid')
    ncolors = int(params.getvalue('NCOLORS',7))
    timeindex = params.getvalue('TIMEINDEX','Default')
    colrange_in = params.getvalue('COLORSCALERANGE','auto')
    # THREDDS allows for the colorscalerange to be set to auto
    # We do not handle that case currently
    if colrange_in == 'auto':
        colrange_in = '-4,4'
    colorrange = tuple([float(a) for a in colrange_in.rsplit(',')])
    save_local_img = bool(int(params.getvalue('SAVE_LOCAL',0)))
    
    # return "doWMS"

    # Might be nicer to just pass a dict to mapdap()
    return mapdap(varname=varname,bbox=bbox,url=url,imgheight=imgheight,imgwidth=imgwidth,
        request=request,time=time,timeindex=timeindex,save_local_img=save_local_img,
        colorrange=colorrange,palette=palette,style=style,ncolors=ncolors)

def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.
    
    cmap: colormap instance, eg. cm.jet. 
    N: Number of colors.
    
    Example
    x = resize(arange(100), (5,100))
    djet = cmap_discretize(cm.jet, 5)
    imshow(x, cmap=djet)
    
    from http://www.scipy.org/Cookbook/Matplotlib/ColormapTransformations
    """
    cdict = cmap._segmentdata.copy()
    # N colors
    colors_i = np.linspace(0,1.,N)
    # N+1 indices
    indices = np.linspace(0,1.,N+1)
    for key in ('red','green','blue'):
                # Find the N colors
        D = np.array(cdict[key])
        I = interpolate.interp1d(D[:,0], D[:,1])
        colors = I(colors_i)
        # Place these colors at the correct indices.
        A = np.zeros((N+1,3), float)
        A[:,0] = indices
        A[1:,1] = colors
        A[:-1,2] = colors
        # Create a tuple for the dictionary.
        L = []
        for l in A:
            L.append(tuple(l))
        cdict[key] = tuple(L)
    # Return colormap object.
    return mpl.colors.LinearSegmentedColormap('colormap',cdict,1024)

def transform_lons(coords,lon,f):
        """ Take bounding box longitudes and transform them so that basemap plots sensibly. """
        """
        Arguments
        coords -- a tuple compose of lonmin,lonmax
        lon -- numpy array of longitudes
        f -- numpy array of the field being plotted

        >>> trans_coords()

        This logic can probably be simplified as it was built incrementally to solve several
        display issues. See tests/allplots.shtml for the tests that drove this function.

        """
        x1,x2 = coords
        lont = lon
        
        # To handle 360 degree plots
        if x2 == x1:
            x2 = x1 + 360
       
        # Basemap doesn't always play well with negative longitudes so convert to 0-360
        lon2360 = lambda x: ((x + 360.) % 360.)
        if x2 < 0:
            x2 = lon2360(x2)
            x1 = lon2360(x1)
            lont = lon2360(lont)

        # If this has resulted in xmin greater than xmax, need to reorder
        if x2 < x1:
            x2 = x2 + 360
        
        # If the start lon is less than zero, then convert to -180:180
        # It's not clear this will ever be executed, given the above code
        if (x1 < 0) or (x2 == x1 and x2 == 180):
            x1 = ((x1 + 180.) % 360.) - 180.
            x2 = ((x2 + 180.) % 360.) - 180.
            lont = ((lont + 180.) % 360.) - 180.

        # If this has resulted in xmin greater than xmax, we need to reorder
        if x2 < x1:
            x2 = x2 + 360

        # If the x2 range is greater than 360 (plots that span both dl and pm)
        # then remap the longitudes to this range
        if x2 > 360:
           idx = lont < x1
           lont[idx] = lont[idx] + 360
       
        # Remap the longitudes for this case too
        if x1 < 0 and x2 > 180:
           idx = lont < x1
           lont[idx] = lont[idx] + 360
       
        # The special case of 0-360
        if x2 == x1:
            if x2 == 0:
                x1 = 0
                x2 = 360
            else:
                x2 = abs(x2)
                x1 = -x2
        
        coords = x1,x2
        # Ensure lons are ascending, and shuffle the field with the same indices
        idx = np.argsort(lont)
        lont = lont[idx]
        ft = f[:,idx]
        ft, lont = addcyclic(ft,lont)
        return coords,lont,ft

def figurePlotDims(imgheight,imgwidth,coords,plot_max_xfrac=0.7,plot_max_yfrac=0.7):
    """
     Given parameters:
        imgwidth,imgheight, 
        coords -- lonmin,latmin,lonmax,latmax,
        the number of plot lons and lats,
        the maximum fraction to be taken up by the plot, 

     compute a new x and y fraction such that the lat/lon aspect ratio is constant.
    """
    lonmin,latmin,lonmax,latmax = coords
    plot_max_height=plot_max_yfrac*imgheight
    plot_max_width=plot_max_xfrac*imgwidth
    nlat = float(latmax-latmin)
    nlon = float(lonmax-lonmin)
    plot_aspect_ratio = plot_max_width/plot_max_height
    latlon_aspect_ratio = (nlon/nlat) * (plot_aspect_ratio)
    desired_aspect_ratio = 1.0
    
    if latlon_aspect_ratio > desired_aspect_ratio:
        # Image is needs to be narrower
        plot_xfrac = (desired_aspect_ratio) * (nlon/nlat) * (plot_max_yfrac) \
            * (float(imgheight)/imgwidth)
        plot_yfrac = plot_max_xfrac
    else:
        # Image is needs to be shorter
        plot_yfrac = (1./desired_aspect_ratio) * (nlat/nlon) * (plot_max_width) \
            * (float(imgwidth)/imgheight)
        plot_xfrac = plot_max_xfrac

    # Ensure we are within the bounds!
    if (plot_yfrac > plot_max_yfrac):
        plot_xfrac = plot_xfrac * plot_max_yfrac/plot_yfrac
        plot_yfrac = plot_max_yfrac
    if (plot_xfrac > plot_max_xfrac):
        plot_yfrac = plot_yfrac * plot_max_xfrac/plot_xfrac
        plot_xfrac = plot_max_xfrac

    return (0.08,0.08,plot_xfrac,plot_yfrac)

def get_pasap_plot_title(dset,
    varname = 'hr24_prcp',
    timestep= 0,
    ):
    """ Given an open pydap object, and some extra information, return a nice
        plot title.
    """
    header = "PASAP: Dynamical Seasonal Outlooks for the Pacific."
    subheader1 = "Outlook based on POAMA 1.5 CGCM adjusted for historical skill"
    subheader2 = "Experimental outlook for demonstration and research only"
    time_var = dset['time']

    if 'units' in time_var.attributes.keys():
        time_units = time_var.attributes['units']
    else:
        time_units = ''
    if 'units' in dset[varname].attributes.keys():
        units = dset[varname].attributes['units']
    else:
        units = ''
    valid_time = datetime.datetime.strftime(
        num2date(time_var[timestep],time_units),"%Y%m%d")
    start_date = datetime.datetime.strftime(
        num2date(dset['init_date'][0],time_units),"%Y%m%d")

    period_label = str(dset['time_label'][timestep])
    titlestring = header + '\n' \
                  + subheader1 + '\n'  \
                  + subheader2 + '\n'  \
                  + "Variable: " + varname + ' (' + units + ')' + '\n' \
                  + 'Model initialised ' + start_date + '\n' \
                  # + 'Forecast period: ' + period_label 

    return titlestring

def mapdap(
    varname = 'hr24_prcp',
    bbox = '-180,-90,180,90',
    url = 'http://opendap.bom.gov.au:8080/thredds/dodsC/PASAP/atmos_latest.nc',
    timeindex = 'Default',
    imgwidth = 256,
    imgheight = 256,
    request = 'GetMap',
    time = 'Default',
    save_local_img = False,
    colorrange = (-4,4),
    palette = 'RdYlGn',
    colorbounds = 'Default',
    style = 'grid',
    ncolors = 10,
    mask = -999,
    plot_mask = True,
    mask_varname = 'mask',
    mask_value = 1.0
    ):
    """ Using Basemap, create a contour plot using some dap available data 
   
        Data is assumed to have dimensions [time,lat,lon] 
            TODO -- deal with other shapes
            TODO -- determine the dimension ordering using CF convention

        varname -- name of variable in opendap file
        bbox -- lonmin,latmin,lonmax,latmax for plot
        url -- OPEnDAP url
        timeindex -- time index to plot
        imgwidth,imgheight -- size of png image to return
        request -- 'GetMap','GetLegend','GetFullFigure'
        time -- time vale to plot. Assumes a particular format."%Y-%m-%dT%H:%M:%S"
        mask -- mask out these values
        if plot_mask is True, mask_varname and mask_value must be given
    
    """
    transparent = True
    lonmin,latmin,lonmax,latmax = tuple([float(a) for a in bbox.rsplit(',')])
   
    # It's not clear there is any point in this. Pydap doesn't actually
    # download data until you subscript 
    
    # FIXME
    url = "http://localhost:8001/ocean_latest.nc"
    
    if url not in cache:
        dset = open_url(url)
    else:
        dset = cache[url]
    
    # Get the correct time.
    time_var = dset['time']
    time_units = time_var.attributes['units']
    available_times = np.array(time_var[:])
    
    

    # TODO there is a potential conflict here between time and timeindex.
    # On the one hand we want to allow using the actual time value.
    # On the other hand we want to make it easy to get a time index
    # without knowing the value.
    timestep=0
    if timeindex == 'Default':
        timestep=0
    else:
        timestep=int(timeindex)
    if time != 'Default':
        dtime = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S" )
        reftime = date2num(dtime,time_units)
        timestep = np.where(available_times >= reftime)[0].min()

    # TODO Get only the section of the field we need to plot
    # TODO Determine lat/lon box indices and only download this slice

    # TODO Set default range (the below does not work)
    #colorrange = np.min(var),np.max(var)
    
    lat = dset['lat'][:]
    lon = dset['lon'][:]
    
    # CHANGED
    var = dset[varname][timestep,:,:]
 
    #xcoords = lonmin,lonmax
    #xcoords,lon,var = transform_lons(xcoords,lon,var)
 
    # TODO
    # Needs mre thought - the idea here is to only grab a slice of the data
    # Need to grab a slightly larger slice of data so that tiling works.
    #lat_idx = (lat > latmin) & (lat < latmax)
    #lon_idx = (lon > lonmin) & (lon < lonmax)
    #lat = dset['lat'][lat_idx]
    #lon = dset['lon'][lon_idx]
    #latdx1 = np.where(lat_idx)[0].min()
    #latdx2 = np.where(lat_idx)[0].max()
    #londx1 = np.where(lon_idx)[0].min()
    #londx2 = np.where(lon_idx)[0].max()
    #var = var[latdx1:latdx2+1,londx1:londx2+1]
    #var = dset[varname][timestep,latdx1:latdx2+1,londx1:londx2+1]

    # todo clean up this logic
    if 'mask' in dset.keys():
        if plot_mask:
            maskvar = dset['mask'][timestep,:,:]
            #maskvar = dset['mask'][timestep,latdx1:latdx2+1,londx1:londx2+1]
            varm = np.ma.masked_array(var,mask=maskvar)
            mask = varm.mask 
    else:
        varm = np.ma.masked_array(var,mask=np.isinf(var))

    xcoords = lonmin,lonmax
    # Call the trans_coords function to ensure that basemap is asked to
    # plot something sensible.
    xcoords,lon,varm = transform_lons(xcoords,lon,varm)
    lonmin,lonmax = xcoords
    varnc = dset[varname]

    try:
        var_units = varnc.attributes['units']
    except KeyError:
       var_units = '' 


    
    # Plot the data
    # For the basemap drawing we can't go outside the range of coordinates
    # WMS requires us to give an empty (transparent) image for these spurious lats
    
    # uc = upper corner, lc = lower corner
    bmapuclon=lonmax
    bmaplclon=lonmin
    bmapuclat=min(90,latmax)
    bmaplclat=max(-90,latmin)
    if bmaplclat==90:
        bmaplclat = 89.0
    if bmapuclat==-90:
        bmapuclat = -89.0

    # TODO set figsize etc here  
    fig = mpl.figure.Figure()
    canvas = FigureCanvas(fig)
    
    ax = fig.add_axes((0,0,1,1),frameon=False,axisbg='k',alpha=0,visible=False)
    m = Basemap(projection='cyl',resolution='c',urcrnrlon=bmapuclon,
        urcrnrlat=bmapuclat,llcrnrlon=bmaplclon,llcrnrlat=bmaplclat,
        suppress_ticks=True,fix_aspect=False,ax=ax)

    DPI=100.0

    # Convert the latitude extents to Basemap coordinates
    bmaplatmin,bmaplonmin = m(latmin,lonmin)
    bmaplatmax,bmaplonmax = m(latmax,lonmax)
    lon_offset1 = abs(bmaplclon - bmaplonmin)
    lat_offset1 = abs(bmaplclat - bmaplatmin)
    lon_offset2 = abs(bmapuclon - bmaplonmax)
    lat_offset2 = abs(bmapuclat - bmaplatmax)
    lon_normstart = lon_offset1 / abs(bmaplonmax - bmaplonmin)
    lat_normstart = lat_offset1 / abs(bmaplatmax - bmaplatmin)
    ax_xfrac = abs(bmapuclon - bmaplclon)/abs(bmaplonmax - bmaplonmin)
    ax_yfrac = abs(bmapuclat - bmaplclat)/abs(bmaplatmax - bmaplatmin)

    # Set plot_coords, the plot boundaries. If this is a regular WMS request,
    # the plot must fill the figure, with whitespace for invalid regions.
    # If it's a full figure, we need to make sure there is space for the legend
    # and also for the text.
    if request == 'GetFullFigure':
        coords = lonmin,latmin,lonmax,latmax
        plot_coords = figurePlotDims(imgheight,imgwidth,coords)
    else:
        plot_coords = (lon_normstart,lat_normstart,ax_xfrac,ax_yfrac)

    m = Basemap(projection='cyl',resolution='c',urcrnrlon=bmapuclon,
        urcrnrlat=bmapuclat,llcrnrlon=bmaplclon,llcrnrlat=bmaplclat,
        suppress_ticks=True,fix_aspect=False,ax=ax)

    ax = fig.add_axes(plot_coords,frameon=False,axisbg='k')

    m.ax = ax
    varm,lonwrap = addcyclic(varm,lon)
    x,y = m(*np.meshgrid(lonwrap[:],lat[:]))

    """ To plot custom colors
    rgb_cmap = mpl.colors.ListedColormap([  
            (0.0,0.0,0.0),
            (0.25,0.25,0.25),
            (0.3,0.25,0.25),
            (0.5,0.5,0.5),
            (0.6,0.5,0.5),
            (0.75,0.75,0.75),
            (0.75,0.85,0.75),
            (1.0,1.0,1.0) ],name='rgbcm')
    default_color_bounds = [-1,-0.75,-0.5,-0.25,0.0,0.25,0.5,0.75,1.0]
    default_norm = mpl.colors.BoundaryNorm(default_color_bounds, rgb_cmap.N)
    m.contourf(x,y,var,cmap=rgb_cmap,norm=default_norm)
    contours = m.contour(x,y,var,cmap=rgb_cmap,norm=default_norm)
    contours.clabel(colors='k')
    """
    colormap = mpl.cm.get_cmap(palette)
    # colormap = cmap_discretize(colormap,ncolors)
    # if colorbounds = 'Default':
    # colorbounds = list(np.arange(colorrange[0],colorrange[1]+increment,increment))
    # else:
    #    colorbounds = list(np.arange(colorrange[0],colorrange[1]+increment,increment))
    #    Do some checks on the size of the list, and fix if we can
    #    pass

    if style == 'contour':
        # Interpolate to a finer resolution
        # TODO: make this sensitive to the chosen domain
        increment = float(colorrange[1]-colorrange[0]) / float(ncolors-2)
        colorbounds = list(np.arange(colorrange[0],colorrange[1]+increment,increment))
        
        
        # CHANGED
        colormap = cmap_discretize(colormap,ncolors)
        
        colvs =[-999]+colorbounds+[999]
        lat_idx = np.argsort(lat)
        lat = lat[lat_idx]
        varm = varm[lat_idx,:]

        data_lonmin = min(lonwrap)
        data_lonmax = max(lonwrap)
        data_latmin = min(lat)
        data_latmax = max(lat)

        new_lons = np.arange(data_lonmin-1.0,data_lonmax+1.0,1.0)
        new_lats = np.arange(data_latmin-1.0,data_latmax+1.0,1.0)
        newx,newy = m(*np.meshgrid(new_lons[:],new_lats[:]))
        x = newx
        y = newy
        
        # Two pass interpolation to deal with the mask.
        # The first pass does a bilinear, the next pass does a nearest neighbour to keep the mask
        # These steps slow down the plotting significantly
        # It's not clear this is working, and the problem is likely solved by
        # ensuring the right mask is used!
        varm_bl = interp(varm, lonwrap[:], lat[:], newx, newy,order=1)
        varm_nn = interp(varm, lonwrap[:], lat[:], newx, newy,order=0)
        varm = varm_bl
        varm[varm_nn.mask == 1] = varm_nn[varm_nn.mask == 1]

        # contourf has an extent keyword (x0,x1,y0,y1)
        # return "mapdap\n"
        # STUCK it gets stuck here (in apache)        
        main_render = m.contourf(x,y,varm[:,:],colorbounds,extend='both',cmap=colormap,ax=ax)
        
        contours = m.contour(x,y,varm,colorbounds,colors='k',ax=ax)
        contours.clabel(colors='k',rightside_up=True,fmt='%1.1f',inline=True)
        
        
        
    elif style == 'grid':
        main_render = m.pcolormesh(x,y,varm[:,:],vmin=colorrange[0],vmax=colorrange[1],
            cmap=colormap,ax=ax)
    elif style == 'grid_threshold':
        increment = float(colorrange[1]-colorrange[0]) / float(ncolors)
        colorbounds = list(np.arange(colorrange[0],colorrange[1]+increment,increment))
        colornorm = mpl.colors.BoundaryNorm(colorbounds,colormap.N)
        main_render = m.pcolor(x,y,varm[:,:],vmin=colorrange[0],vmax=colorrange[1],
            cmap=colormap,ax=ax,norm=colornorm)
    else:
        main_render = m.pcolormesh(x,y,varm[:,:],vmin=colorrange[0],vmax=colorrange[1],
            cmap=colormap,ax=ax)


    fig.set_dpi(DPI)
    fig.set_size_inches(imgwidth/DPI,imgheight/DPI)

    title_font_size = 9
    tick_font_size = 8
    if request == 'GetFullFigure':
        # Default - draw 5 meridians and 5 parallels
        n_merid = 5
        n_para = 5

        # base depends on zoom
        mint = (lonmax - lonmin)/float(n_merid)
        base = mint
        meridians = [lonmin + i*mint for i in range(n_merid)]
        meridians = [ int(base * round( merid / base)) for merid in meridians]
        
        # Some sensible defaults for debugging
        #meridians = [45,90,135,180,-135,-90,-45]

        pint = int((latmax - latmin)/float(n_para))
        base = pint
        parallels = [latmin + i*pint for i in range(1,n_para+1)] 
        parallels = [ int(base * round( para / base)) for para in parallels]
        #parallels = [-60,-40,-20,0,20,40,60]
        #parallels = [((parallel + 180.) % 360.) - 180. for parallel in parallels]
        m.drawcoastlines(ax=ax)
        
        m.drawmeridians(meridians,labels=[0,1,0,1],fmt='%3.1f',fontsize=tick_font_size)
        m.drawparallels(parallels,labels=[1,0,0,0],fmt='%3.1f',fontsize=tick_font_size)
        m.drawparallels([0],linewidth=1,dashes=[1,0],labels=[0,1,1,1],fontsize=tick_font_size)
        titlex,titley = (0.05,0.98)
        
        # CHANGED 
        # STUCK getting an error somewhere in this function
        # title = get_pasap_plot_title(dset,varname=varname,timestep=timestep)
        title = "We're getting errors in the get title function"
        fig.text(titlex,titley,title,va='top',fontsize=title_font_size)
   
    colorbar_font_size = 8
    if request == 'GetLegendGraphic':
        # Currently we make the plot, and then if the legend is asked for
        # we use the plot as the basis for the legend. This is not optimal.
        # Instead we should be making the legend manually. However we need
        # to set up more variables, and ensure there is a sensible min and max.
        # See the plot_custom_colors code above
        fig = mpl.figure.Figure(figsize=(64/DPI,256/DPI))
        canvas = FigureCanvas(fig)
        # make some axes
        cax = fig.add_axes([0,0.1,0.2,0.8],axisbg='k')
        # put a legend in the axes
        
        
        cbar = fig.colorbar(main_render,cax=cax,extend='both',format='%1.1f')
        cbar.set_label(var_units,fontsize=colorbar_font_size)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(colorbar_font_size)
        # i.e. you don't need to plot the figure...
        #fig.colorbar(filled_contours,cax=cax,norm=colornorm,boundaries=colvs,values=colvs,
        #   ticks=colorbounds,spacing='proportional')
    elif request == 'GetFullFigure':
        # Add the legend to the figure itself.
        # Figure layout parameters
        # plot_coords = tuple with (xi,yi,dx,dy)
        # legend_coords = tuple with (xi,yi,dx,dy) as per mpl convention
        # First change the plot coordinates so that they do not cover the whole image
        legend_coords = (0.8,0.1,0.02,plot_coords[3])
        cax = fig.add_axes(legend_coords,axisbg='k')
        cbar = fig.colorbar(main_render,cax=cax,extend='both')
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(colorbar_font_size)
        cbar.set_label(var_units,fontsize=colorbar_font_size)
        transparent=False
        # Experimenting here with custom color map and ticks. Assigning everything manually
        # (e.g. ticks=[-2,-1,0,1,2]) is easy. Doing it in an automated way given a range is
        # hard...
        #fig.colorbar(filled_contours,cax=cax,boundaries=colvs,ticks=colorbounds)
        #,norm=colornorm,#boundaries=colvs,values=colvs,        #extend='both')
           
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata,format='png',transparent=transparent)
    
    if save_local_img:
        fig.savefig('map_plot_wms_output.png',format='png')
        return

    if url not in cache:
        cache[url] = dset

    value = imgdata.getvalue()

    #imgdata.close()
    fig = None
    
    
    return value

def ocean_mask_test():
        params = cgi.FieldStorage()
        for name, value in {
            "INVOCATION" : "terminal",
            "SAVE_LOCAL": "1",
            "REQUEST" : "GetFullFigure",
            "BBOX" : "00,-90,360,90",
            # "WIDTH" : "640",
            # "HEIGHT" : "300",
            # CHANGED
            "WIDTH" : "800",
            "HEIGHT" : "600",                    
            "DAP_URL" : 'http://opendap.bom.gov.au:8080/thredds/dodsC/PASAP/ocean_latest.nc',
            "LAYER" : 'SSTA',
            "STYLE" : 'contour'
            #"STYLE" : 'grid'
        }.items():
            params.list.append(cgi.MiniFieldStorage(name, value))
        doWMS(params)

def atmos_mask_test():
        params = cgi.FieldStorage()
        for name, value in {
            "INVOCATION" : "terminal",
            "SAVE_LOCAL": "1",
            "REQUEST" : "GetFullFigure",
            "BBOX" : "70,-50,180,-5",
            "WIDTH" : "640",
            "HEIGHT" : "300",
            "DAP_URL" : 'http://opendap.bom.gov.au:8080/thredds/dodsC/PASAP/atmos_latest.nc',
            "LAYER" : 'hr24_prcp',
            "STYLE" : 'contour'
            #"STYLE" : 'grid'
        }.items():
            params.list.append(cgi.MiniFieldStorage(name, value))
        doWMS(params)


# if __name__ == '__main__':
#     if 'TERM' in os.environ:
#         print "Running from terminal"
#         os.environ['INVOCATION'] = 'terminal'
# 
#         # Some test parameters for debugging
#         ocean_mask_test()
#         # atmos_mask_test()
# 
#     elif 'CGI' in os.environ.get('GATEWAY_INTERFACE',''):
#         os.environ['INVOCATION'] = 'cgi'
#         import wsgiref.handlers
#         wsgiref.handlers.CGIHandler().run(application)
#     else:
#         os.environ['INVOCATION'] = 'wsgi'
#         pass
        
if __name__ == '__main__':
    from paste import httpserver
    # os.environ['INVOCATION'] = 'wsgi'
    # httpserver.serve(application, host='127.0.0.1', port='2345')
    httpserver.serve(application, host='0.0.0.0', port='2345')
