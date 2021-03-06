import modules.plotting.plotting_controller as pc

defaults = { "request":"GetMap",
              "version":"0.0.1",
                      "bbox" : {  "min_lat" : "-90.0",
                                      "min_lon" : "-180.0",
                                      "max_lat" : "90.0",
                                      "max_lon" : "180.0" 
                                } ,
                          "width" : "256",
                          "height" : "256",
                          "layers" : "hr24_prcp",
                          "styles" : "grid",
                          "crs" : "EPSG:4283",
                          "format" : "png",
                          "time" : "Default",
                          "time_index" : "Default",
                        "source_url" : "http://localhost:8001/atmos_latest.nc",
                          "color_scale_range" : ["auto", ],
                          "n_colors" : ["7", ],
                          "palette" : "jet",
                          "line_style" : None
                        }
        
param = { "bbox" : {  "min_lat" : "-90.0",
                      "min_lon" : "0.0",
                      "max_lat" : "90.0",
                      "max_lon" : "360.0" 
                    } ,
        "layers" : ["hr24_prcp", ] ,
        #"layers" : ["tsair", ] ,
        "styles" : ["contour", ] ,
        "crs" : {   "name" : "EPSG" ,
                    "identifier" : "4283" 
                } ,
        "width" : "1024" ,
        "height" : "768" ,
   #     "format" : "png" ,
        "time" : "Default" ,
        "time_index" : "Default" ,
#        "source_url" : "http://localhost:8001/vertical_line.nc",
        "source_url" : "http://localhost:8001/atmos_latest.nc",
        #"source_url" : "http://localhost:8001/ocean_latest.nc",
        "color_scale_range" : ["-10", "10", ] ,
        "n_colors" : ["10", ] ,
        "palette" : "jet" ,
        #"palette" : "YlOrBr"
        "colors" : ["r","#11ffcc","g", "#123abc", "#abc123","#abcdef" , "m"] ,
        "color_levels" : ["-2", "-1","0" , "2.5" ,"3.0", "5" , "10" , "15"] ,
        "min_color" : "yellow" ,
        #"max_color" : "#00aaff",
       # "line_style" : "dotted"
}


        
#c = pc.PlottingController(param)
#output = c.get_contour()

import pylab

pylab.ion()

d,f = pc.get_contour(param,defaults)
#d,f = pc.get_legend(param,defaults)
#d,f = pc.get_full_figure(param,defaults)
#print d

print "format: %s" % f
img = open("test.png","w")
img.write(d)
img.close()


