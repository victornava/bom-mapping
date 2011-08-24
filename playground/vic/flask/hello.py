from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/count')
def count():
    reply = ""
    for number in range(7):
        reply += "number %d<br />" % number
    return reply

if __name__ == '__main__':
    app.run()
    