import modules.plotting.plotting_controller as pc


        
param = { "bbox" : {  "min_lat" : "-90.0",
                      "min_lon" : "0.0",
                      "max_lat" : "90.0",
                      "max_lon" : "360.0" 
                    } ,
        #"layers" : ["lwe_thickness", ] ,
        #"layers" : ["hr24_prcp", ] ,
        "layers" : ["temp", ] ,
        "styles" : ["contour", ] ,
        "crs" : {   "name" : "EPSG" ,
                    "identifier" : "4283" 
                } ,
        "width" : "1024" ,
        "height" : "768" ,
        "format" : "png" ,
        "time" : "Default" ,
        "time_index" : "Default" ,
        #"source_url" : "/home/saurabh/Downloads/test.nc",
        #"source_url" : "/home/saurabh/Downloads/atmos_latest.nc",
        "source_url" : "http://yoursoft06.cs.rmit.edu.au:8001/test.nc",
        #"source_url" : "http://ensembles.ecmwf.int/thredds/dodsC/demeter-non-agg/229/MM_229_mon_2001.nc",
        #"source_url" : "http://opendap.jpl.nasa.gov/opendap/GeodeticsGravity/tellus/L3/land_mass/netcdf/GRACE.CSR.LAND.RL04.DS.G300KM.nc",
        "color_scale_range" : ["-10", "10", ] ,
        "n_colors" : ["10", ] ,
        "palette" : "jet"
        #"palette" : "YlOrBr"
}
        
#c = pc.PlottingController(param)
#output = c.get_contour()

d = pc.get_contour(param)
#d = pc.get_legend(param)
#d = pc.get_full_figure(param)
#print d

img = open("test.png","w")
img.write(d)
img.close()
