#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler, authenticated

class IndexHandler(RequestHandler):
    @authenticated
    def get(self):
        self.write("HELLO USER")
