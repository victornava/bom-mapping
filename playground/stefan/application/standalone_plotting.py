import modules.plotting.plotting_controller as pc



param = { "bbox": { "min_lat" : -90.0,
                    "min_lon" : 0.0,
                    "max_lat" : 90.0,
                    "max_lon" : 360.0 
                   } ,
          "width" : 300 ,
          "height" : 400 ,
          "layers" : ["hr24_prcpa", ] ,
          "styles" : ["contour", ] ,
          "crs" : {   "name" : "EPSG" ,
                      "identifier" : "4283" 
                  } ,
          "format" : "png" ,
          "time" : "Default" ,
          "time_index" : "Default" ,
          "source_url" : "http://localhost:8001/atmos_latest.nc",
          "color_range" : (-10,10) ,
          "n_color" : 10 ,
          "palette" : "jet"
        }
        
c = pc.PlottingController(param)
output = c.get_contour()