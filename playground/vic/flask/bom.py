import sys
from flask import Flask, make_response
from pprint import pprint
app = Flask(__name__)

@app.route('/')
def index():
    html = 'Try <a href="/img">img</a> or <a href="/getmap">getmap</a>'
    return html


@app.route('/img')
def img():
    img = open('oldman.png').read()
    resp = make_response(img)
    resp.headers['Content-Type'] = 'image/png'
    return resp
    
@app.route('/getmap')
def getmap():
    img  = generate_map()
    resp = make_response(img)
    resp.headers['Content-Type'] = 'image/png'
    return resp
    
#Fake map generator :)    
def generate_map():
    return open('oldman.png').read()

if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    # app.run()

