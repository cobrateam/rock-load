#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler

class LoginHandler(RequestHandler):
    def get(self):
        self.render("rockload/apps/auth/login.html")

