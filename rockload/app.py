#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import os
from os.path import join, abspath, dirname, expanduser, exists

import tornado.web
import tornado.ioloop
from tornado.options import parse_config_file

from rockload.handlers import MainHandler, AuthLoginHandler, AuthLogoutHandler

class RockLoadApp(tornado.web.Application):

    def __init__(self, conf_file=None, custom_handlers=None):
        if conf_file is None:
            conf_file = RockLoadApp.get_conf_file(conf_file)

        parse_config_file(conf_file)

        handlers = [
            (r'/', MainHandler),
            (r'/login', AuthLoginHandler),
            (r'/logout', AuthLogoutHandler)
        ]

        settings = {
            "cookie_secret": "QmVybmFyZG8gSGV5bmVtYW5uIE5hc2NlbnRlcyBkYSBTaWx2YQ==",
            "login_url": "/login",
        }

        super(RockLoadApp, self).__init__(handlers, **settings)

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
