from flask import Flask, make_response
from pprint import pprint
app = Flask(__name__)

@app.route('/')
def index():
    return 'Try <a href="/img">img</a>'


@app.route('/img')
def img():
    img = open('oldman.png').read()
    resp = make_response(img)
    resp.headers['Content-Type'] = 'image/png'
    return resp
    
@app.route('/getmap')
def getmap():
    img = open('oldman.png').read()
    resp = make_response(img)
    resp.headers['Content-Type'] = 'image/png'
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    # app.run()

