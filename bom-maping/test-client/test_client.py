import sys
from flask import Flask, make_response, request
app = Flask(__name__)

@app.route('/')
def index():
    links = ["ours","prototype"]
    
    html = ""
    for link in links:
        html += "<div><a href="+link+">"+link+"</a></div>"
    return html
    
@app.route('/ours')
def new():
    url = "http://localhost:8007/?REQUEST=GetFullFigure&DAP_URL=http://localhost:8001/ocean_latest.nc&LAYERS=SSTA&TIMEINDEX=0&COLORSCALERANGE=-10,10&WIDTH=800&HEIGHT=600&BBOX=0,-90,360,90&STYLE=contour"
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
    app.run(host='0.0.0.0', port=port)