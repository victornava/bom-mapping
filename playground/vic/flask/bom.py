import sys
from flask import Flask, make_response, request
app = Flask(__name__)

@app.route('/')
def index():
    html = 'Try <a href="/img">img</a> or <a href="/getmap">getmap</a> or <a href="/params">params</a>'
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


@app.route('/params')
def params():
    args = request.args
    keys = args.keys()
    html = "<h3>Params</h3>"
    
    if len(keys) == 0:
        html += 'Try passing some params like <a href="/params?fruit=mango&color=yellow&size=big">this</a><br />'
    else:        
        for k in keys:
            html += k+': '+args.get(k)+'<br />'
    return html
    
#Fake map generator :)
# we'll replace this with the real method
def generate_map():
    return open('oldman.png').read()

# can pass the port number as argument
if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    # app.run()