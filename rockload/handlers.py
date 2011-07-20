#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.auth
from tornado.options import options

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return user_id

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write('Welcome %s' % self.get_current_user())

class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
    
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie('user', user["email"])
        self.redirect(self.get_argument("next", "/"))

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

