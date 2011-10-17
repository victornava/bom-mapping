available = {
    "image_formats" : ["png", "jpeg"],
    "capabilities_formats": ["xml"],
    "version" : "1.3.0",
    "service" : "wms",
    "exception_formats": ["xml"],
    "requests" : ["GetMap", "GetFullFigure", "GetLegend", "GetCapabilities"],
    "styles": ["grid", "contour", "grid_treshold"],
    "request_methods" : ["GET","POST"]
    }

defaults = {
    "request":"GetMap",
    "version":"0.0.1",
    "bbox" : "-180,-90,180,90",
    "width" : "256",
    "height" : "256",
    "layers" : "hr24_prcp",
    "styles" : "grid",
    "crs" : "EPSG:4283",
    "format" : "image/png",
    "time" : "Default",
    "time_index" : "Default",
    "source_url" : "http://localhost:8001/atmos_latest.nc",
    # "source_url" : "http://opendap.bom.gov.au:8080/thredds/dodsC/PASAP/atmos_latest.nc",
    "color_scale_range" : "auto",
    "n_colors" : "7",
    "palette" : "jet",
    "line_style" : "solid"
    }
    
capabilities_defaults = {
    "format" : "text/xml",
    "version" : "1.3.0",
    "service" : "wms"
    }

# Service Info

service_basic_info = {
    "name": "WMS",
    "title": "BOM - Australia",
    "abstract" : "Map Overlay Web Service for the Australian Bureu of Meteorology",
    "keywordlist" : ["BOM","Contour Plot"],
    "online_resource_url" : "http://bom.gov.au",
    "fees" : "0",
    "access_constraints" : "none",
    "layer_limit" : "0",
    "max_width" : "0",
    "max_height" : "0"
    }

# Contact Information

contact_info = {
    "person" : {
        "name" : "Andrew",
        "organization" : "BOM" },
    "contact_address" : {
        "address_type" : "postal",
        "address" : "Collin's street",
        "city" : "Melbourne",
        "state" : "VIC",
        "postcode" : "3000",
        "country" : "Australia"},
    "phone" : "+61 XXXX XXXX",
    "email" : "xyz@bom.gov.au"
    }
