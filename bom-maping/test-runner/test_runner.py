import sys
from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def index():
    # get the path of the features dir
    features_path = os.path.dirname(os.path.abspath(__file__)) + "/../features"
    # run the cucumber comand and spit out the reply
    return os.popen("cucumber " + features_path +" --format html").read()
    
# can pass the port number as argument
if __name__ == '__main__':
    port = 8009
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='0.0.0.0', port=port)