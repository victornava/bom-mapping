import web

urls = (
    '/', 'hello', 
    '/hola', 'hola'
)

app = web.application(urls, globals())

class hello:
    def GET(self):
        return '<h1>Hello, stefan I\'m running a webservice form python</h1>'
        
        
class hola:
    def GET(self):
        return '<h1>Hola, stefan I\'m running a webservice form python</h1>'

if __name__ == "__main__":
    app.run()