# -*- coding: utf-8 -*-

import optparse

import tornado.ioloop
from tornado.httpserver import HTTPServer

from aero.app import AeroApp

DEFAULT_IP = "0.0.0.0"
DEFAULT_PORT = 3333

def main():
    '''Runs rockload server with the specified arguments.'''
    parser = optparse.OptionParser(usage="rockload-server or type rockload-server -h (--help) for help", description=__doc__, version="0.1.0")
    parser.add_option("-p", "--port", type="int", dest="port", default=DEFAULT_PORT, help = "The port to run this thumbor instance at [default: %default]." )
    parser.add_option("-i", "--ip", dest="ip", default=DEFAULT_IP, help = "The host address to run this thumbor instance at [default: %default]." )
    parser.add_option("-r", "--reports", dest="report_dir", default='./reports', help = "The directory where rockload will keep the reports. May be absolute or relative. [default: %default]." )
    parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help = "Indicates that the app should be run in debug mode[default: %default]." )
    parser.add_option("-m", "--mongodb", dest="mongo_db", default="rockload", help = "Name of the mongo database to use [default: %default]." )
    parser.add_option("-n", "--mongohost", dest="mongo_host", default="localhost", help = "Host of the mongo database to use [default: %default]." )
    parser.add_option("-o", "--mongoport", dest="mongo_port", type="int", default=12345, help = "Port of the mongo database to use [default: %default]." )

    (options, args) = parser.parse_args()

    port = options.port
    ip = options.ip
    debug = options.debug
    report_dir = options.report_dir

    handlers = [
        (r"/reports/(.*)", tornado.web.StaticFileHandler, {"path": report_dir})
    ]

    settings = {
        "cookie_secret": "d2hhdCBhIG5pY2Ugc2VjcmV0IGtleQ==",
        "login_url": "/login",
        "debug": debug,
        'report_dir': report_dir,
        'mongo_db': options.mongo_db,
        'mongo_host': options.mongo_host,
        'mongo_port': options.mongo_port,
        'installed_apps':  [
            'rockload.apps.main',
            'rockload.apps.auth',
            'rockload.apps.mongo',
            'rockload.apps.base',
            'aero.apps.healthcheck',
        ]
    }

    app = AeroApp(handlers, **settings)

    run_app(ip, port, app)

def run_app(ip, port, app):
    server = HTTPServer(app)
    server.bind(port, ip)
    server.start(1)

    try:
        print '-- running rockload at %s:%s --' % (ip, port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print
        print "-- rockload closed by user interruption --"

if __name__ == "__main__":
    main()
