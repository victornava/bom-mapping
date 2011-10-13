import sys
from flask import *
import config
app = Flask(__name__)

@app.route('/')
def index():
    content = render_template("test.html", config=config)
    response = make_response(content)
    response.headers['Content-Type'] = "text/html"
    return response

# can pass the port number as argument
if __name__ == '__main__':
    port = 8010
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.debug = True
    app.run(host='0.0.0.0', port=port)
