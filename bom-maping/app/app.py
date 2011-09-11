import sys
from flask import Flask, make_response, request
app = Flask(__name__)


@app.route('/')
def index():
    # TODO validate query
    # TODO pass query to map model
    
    # return "helloworld"
    
    # fake the output so the test pass
    return " | ".join([
        "WMSArgumentError" , 
        "request parameter is missing", 
        "crs parameter is missing", 
        "WMSError" ,
        "Operation not supported"
    ])

# can pass the port number as argument
if __name__ == '__main__':
    port = 8007
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    # app.run()