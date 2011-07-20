#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import signal
import optparse
import logging

import tornado.ioloop
from tornado.httpserver import HTTPServer

from rockload import __version__
from rockload.app import RockLoadApp

ip = "0.0.0.0"
port = 8888
conf = None
server = None

def __kill_server():
    print 'stopping server...'
    server.stop()
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.stop()
    ioloop._stopped = False

def handle_sigterm(signum, frame):
    __kill_server()
    print "server stopped"

def handle_sighup(signum, frame):
    __kill_server()
    print 'restarting server...'
    run_app(ip, port, conf)

def main():
    '''Runs rockload server with the specified arguments.'''
    global server
    global ip
    global port
    global conf

    parser = optparse.OptionParser(usage="rockload or type rockload -h (--help) for help", description=__doc__, version=__version__)
    parser.add_option("-p", "--port", type="int", dest="port", default=8888, help = "The port to run this rockload instance at [default: %default]." )
    parser.add_option("-i", "--ip", dest="ip", default="0.0.0.0", help = "The host address to run this rockload instance at [default: %default]." )
    parser.add_option("-c", "--conf", dest="conf", default="", help = "The path of the configuration file to use for this rockload instance [default: %default]." )
    parser.add_option("-l", "--log-level", dest="log_level", default="warning", help = "The log level to be used. Possible values are: debug, info, warning, error, critical or notset. [default: %default]." )

    (options, args) = parser.parse_args()

    if not signal.getsignal(signal.SIGHUP):
        signal.signal(signal.SIGHUP, handle_sighup)
    if not signal.getsignal(signal.SIGTERM):
        signal.signal(signal.SIGTERM, handle_sigterm)

    port = options.port
    ip = options.ip
    conf = options.conf or None
    log_level = options.log_level

    run_app(ip, port, conf, log_level)

def run_app(ip, port, conf, log_level):
    global server

    logging.basicConfig(level=getattr(logging, log_level.upper()))

    application = RockLoadApp(conf)

    server = HTTPServer(application)
    server.bind(port, ip)
    server.start()

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print
        print "-- rockload closed by user interruption --"

if __name__ == "__main__":
    main()

