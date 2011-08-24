#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
import tornado.auth

from rockload.apps.base.handlers import BaseHandler

class LoginHandler(RequestHandler):
    def get(self):
        self.render("rockload/apps/auth/login.html")

class GoogleLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
    
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")

        self.set_secure_cookie("user", user['email'])
        self.set_secure_cookie("username", user['name'])
        self.redirect(self.get_argument("next", "/"))

