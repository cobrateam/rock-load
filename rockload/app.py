#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import os
from os.path import join, abspath, dirname, expanduser, exists

import tornado.web
import tornado.ioloop
import tornado.database
from tornado.options import parse_config_file, define, options

from rockload.handlers import MainHandler, AuthLoginHandler, AuthLogoutHandler, CreateProjectHandler, ProjectTestsListHandler
from rockload.handlers import NewTestHandler

define("mysql_host", default="127.0.0.1:3306", help="rockload database host")
define("mysql_database", default="rockload", help="rockload database name")
define("mysql_user", default="root", help="rockload database user")
define("mysql_password", default="", help="rockload database password")

class RockLoadApp(tornado.web.Application):

    def __init__(self, conf_file=None):
        if conf_file is None:
            conf_file = RockLoadApp.get_conf_file(conf_file)

        parse_config_file(conf_file)

        handlers = [
            (r'/', MainHandler),
            (r'/login', AuthLoginHandler),
            (r'/logout', AuthLogoutHandler),
            (r'/projects/new', CreateProjectHandler),
            (r'/projects/(\d+)', ProjectTestsListHandler),
            (r'/projects/(\d+)/tests/new', NewTestHandler)
        ]

        settings = {
            "cookie_secret": "QmVybmFyZG8gSGV5bmVtYW5uIE5hc2NlbnRlcyBkYSBTaWx2YQ==",
            "login_url": "/login",
            "template_path": join(dirname(__file__), "templates"),
            "static_path": join(dirname(__file__), "static"),
        }

        super(RockLoadApp, self).__init__(handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

    @classmethod
    def get_conf_file(cls, conf_file):
        lookup_conf_file_paths = [
            os.curdir,
            expanduser('~'),
            '/etc/',
            dirname(__file__)
        ]
        for conf_path in lookup_conf_file_paths:
            conf_path_file = abspath(join(conf_path, 'rockload.conf'))
            if exists(conf_path_file):
                return conf_path_file

        raise ConfFileNotFoundError('rockload.conf file not passed and not found on the lookup paths %s' % lookup_conf_file_paths)

class ConfFileNotFoundError(RuntimeError):
    pass


def main():
    pass

if __name__ == '__main__':
    main()
