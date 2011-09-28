import modules.plotting.plotting_controller as pc


param = { "bbox": { "min_lat" : "-90",
                    "min_lon" : "-45.0",
                    "max_lat" : "-0.0",
                    "max_lon" : "45.0"
                   } ,
          "width" : "1024" ,
          "height" : "768" ,
          "layers" : ["hr24_prcp", ] ,
#          "layers" : ["tsair", ] ,
#          "layers" : ["SSTA", ] ,
          "styles" : ["contour", ] ,
          "crs" : {   "name" : "EPSG" ,
                      "identifier" : "4283" 
                  } ,
          "format" : "png" ,
          "time" : "Default" ,
          "time_index" : "Default" ,
          "source_url" : "http://localhost:8001/atmos_latest.nc",
#          "source_url" : "http://localhost:8001/ocean_latest.nc",
          "color_range" : "-10, 10" ,
          "n_color" : "9" ,
#          "palette" : "jet"
          "palette" : "YlOrBr"
        }
        
#c = pc.PlottingController(param)
#output = c.get_contour()

#d = pc.get_contour(param)
#d = pc.get_legend(param)
d = pc.get_full_figure(param)
#print d

img = open("test.png","w")
img.write(d)
img.close()