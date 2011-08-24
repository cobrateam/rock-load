#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return user_id

    def get_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username


