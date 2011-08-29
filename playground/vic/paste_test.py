def application(environ, start_response):
    status = '200 OK'
    output = 'All good'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port='2345')