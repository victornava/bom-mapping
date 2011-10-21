import sys
from flask import Flask, make_response, request
app = Flask(__name__)

@app.route('/')
def index():
    links = ["ours","prototype", "custom"]
    
    html = ""
    for link in links:
        html += "<div><a href="+link+">"+link+"</a></div>"
    return html
    
@app.route('/ours')
def new():
    
    # url = "http://localhost:8007/?REQUEST=GetMap&source_url=http://localhost:8001/ocean_latest.nc&layers=SSTA&time_index=0&colorscalerange=-10,10&width=800&height=600&bbox=0,-90,360,90&styles=contour&time=Default&palette=jet&color_range=-10,10&n_color=10&format=png"
    url = "http://localhost:8007/?"
    
    params = {
        "request":"GetMap",
        "bbox":"0,-90,360,90",
        "width": "300",
        "height": "400",
        # "layers": "hr24_prcp",
        "layers" : "SSTA",
        "styles" : "contour",
        "crs" : "EPSG:4283",
        "format" : "image/png" ,
        "time" : "Default" ,
        "time_index": "Default" ,
        # "source_url": "http://localhost:8001/atmos_latest.nc",
        "source_url" : "http://localhost:8001/ocean_latest.nc",
        "color_range" : "-10,10" ,
        "n_color" : "10" ,
        "palette" : "jet"
    }
    
    url += "&".join("=".join(i) for i in params.items())
    return "<a href="+url+">"+url+"</a>"
    
@app.route('/custom')
def custom():
    
    url = "http://localhost:8007/?"
    
    params = {
        "request":"GetMap",
        "bbox":"-180,-90,1800,90",
        "width": "694",
        "height": "573",
        "layers": "hr24_prcp",
        #"layers" : "SSTA",
        "styles" : "contour",
        "crs" : "EPSG:4283",
        "format" : "png" ,
        "time" : "Default" ,
        "time_index": "Default" ,
        "source_url": "http://localhost:8001/atmos_latest.nc",
        #"source_url" : "http://localhost:8001/ocean_latest.nc",
        "palette" : "jet",
        # Cust colors here
        "custom_colors" : "%23aabbcc,%23abc123,b,%23123123,m",
        "custom_levels" : "0,2.5,3.0,5,10,15",
        "custom_min" : "cyan",
        "custom_max" : "yellow"
    }
    
    url += "&".join("=".join(i) for i in params.items())
    return "<a href="+url+">"+url+"</a>"

@app.route('/prototype')
def prototype():
    url = "http://localhost:8006/?REQUEST=GetFullFigure&DAP_URL=http://localhost:8001/ocean_latest.nc&LAYERS=SSTA&TIMEINDEX=0&COLORSCALERANGE=-10,10&WIDTH=800&HEIGHT=600&BBOX=0,-90,360,90&STYLE=contour"
    return "<a href="+url+">"+url+"</a>"
    
# can pass the port number as argument
if __name__ == '__main__':
    port = 8008
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='127.0.0.1', port=port)