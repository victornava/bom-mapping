import sys
from flask import Flask, make_response, request
app = Flask(__name__)

@app.route('/')
def index():
    return "hello"
    
    
# can pass the port number as argument
if __name__ == '__main__':
    port = 8007
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    # app.run()

        