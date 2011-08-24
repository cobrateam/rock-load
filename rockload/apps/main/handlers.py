#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import authenticated

from rockload.apps.base.handlers import BaseHandler

class IndexHandler(BaseHandler):
    @authenticated
    def get(self):
        self.write("HELLO USER")
