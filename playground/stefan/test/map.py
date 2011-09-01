#!/usr/bin/python


import sys
import os
os.environ['HOME'] = '/var/www'
import lala_bom as ec


def application(environ, start_response):
    status = '200 OK'
    output = ec.createMap()
    
#    print >> sys.stderr, output
    
#    response_headers = [('Content-type', 'text/plain'),
#                        ('Content-Length', str(len(output)))]
                        
    response_headers = [('Content-type', 'image/png'),
                        ('Content-Length', str(len(output)))]
                        
    #print >> sys.stderr, output
    
    start_response(status, response_headers)

    return [output]
    

if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port='8080')