# -*- coding: utf-8 -*-

import optparse

import tornado.ioloop
from tornado.httpserver import HTTPServer

from aero.app import AeroApp

ip = "0.0.0.0"
port = 9999
server = None

def main():
    '''Runs rockload server with the specified arguments.'''
    global server
    global ip
    global port

    parser = optparse.OptionParser(usage="thumbor-urls or type thumbor-urls -h (--help) for help", description=__doc__, version="0.1.0")
    parser.add_option("-p", "--port", type="int", dest="port", default=8888, help = "The port to run this thumbor instance at [default: %default]." )
    parser.add_option("-i", "--ip", dest="ip", default="0.0.0.0", help = "The host address to run this thumbor instance at [default: %default]." )

    (options, args) = parser.parse_args()

    port = options.port
    ip = options.ip

    app = AeroApp(apps=[
        'aero.apps.healthcheck',
        'rockload.apps.main'
    ])

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
