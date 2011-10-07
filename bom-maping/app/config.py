available = {
    "formats": ["png", "jpeg"],
    "image_formats": ["png", "jpeg"],
    "capabilities_formats": ["xml"],
    "exception_formats": ["xml"],
    "requests" : ["GetMap", "GetFullFigure", "GetLeyend", "GetCapabilities"],
    "styles": ["grid", "contour", "grid_treshold"]
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
    "format" : "png",
    "time" : "Default",
    "time_index" : "Default",
    "source_url" : "http://localhost:8001/atmos_latest.nc",
    # "source_url" : "http://opendap.bom.gov.au:8080/thredds/dodsC/PASAP/atmos_latest.nc",
    "color_scale_range" : "auto",
    "n_colors" : "7",
    "palette" : "jet"
    }