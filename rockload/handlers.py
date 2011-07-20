#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.auth
from tornado.options import options

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return user_id

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write('Welcome %s' % self.get_current_user())

def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        user = self.db.get("SELECT * FROM user WHERE email = %s",
                             user["email"])
        if not user:
            any_user = self.db.get("SELECT * FROM user LIMIT 1")
            if not any_user:
                user_id = self.db.execute(
                    "INSERT INTO user(email, name) VALUES (%s,%s)",
                    user["email"], user["name"])
            else:
                self.redirect("/")
                return
        else:
            user_id = user["id"]
        self.set_secure_cookie("user", str(user_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

