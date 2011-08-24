# -*- coding: utf-8 -*-

import optparse

import tornado.ioloop
from tornado.httpserver import HTTPServer

from aero.app import AeroApp

DEFAULT_IP = "0.0.0.0"
DEFAULT_PORT = 9999
server = None

def main():
    '''Runs rockload server with the specified arguments.'''
    global server
    global ip
    global port

    parser = optparse.OptionParser(usage="rockload-server or type rockload-server -h (--help) for help", description=__doc__, version="0.1.0")
    parser.add_option("-p", "--port", type="int", dest="port", default=DEFAULT_PORT, help = "The port to run this thumbor instance at [default: %default]." )
    parser.add_option("-i", "--ip", dest="ip", default=DEFAULT_IP, help = "The host address to run this thumbor instance at [default: %default]." )

    (options, args) = parser.parse_args()

    port = options.port
    ip = options.ip

    settings = {
        "cookie_secret": "d2hhdCBhIG5pY2Ugc2VjcmV0IGtleQ==",
        "login_url": "/login"
    }

    app = AeroApp(apps=[
        'rockload.apps.main'
        'rockload.apps.auth',
        'rockload.apps.base',
        'aero.apps.healthcheck',
    ], **settings)

    run_app(ip, port, app)

def run_app(ip, port, app):
    global server

    server = HTTPServer(app)
    server.bind(port, ip)
    server.start(1)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print
        print "-- rockload closed by user interruption --"

if __name__ == "__main__":
    main()
