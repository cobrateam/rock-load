#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.auth

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM user WHERE id = %s", int(user_id))

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        projects = self.db.query("SELECT * FROM project order by name")
        self.render("home.html", user=user, projects=projects)

class ProjectTestsListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, project_id):
        project = self.db.get("SELECT * FROM project WHERE id = %s", int(project_id))
        if not project: raise tornado.web.HTTPError(404)
        self.render("project_list.html", user=self.get_current_user(), project=project, tests=None)

class CreateProjectHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("create_project.html", user=self.get_current_user())

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument("name")

        self.db.execute(
                "INSERT INTO project (name)"
                "VALUES (%s)",
                name)

        self.redirect('/')

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
        db_user = self.db.get("SELECT * FROM user WHERE email = %s",
                             user["email"])
        if not db_user:
            user_id = self.db.execute(
                "INSERT INTO user(email, name) VALUES (%s,%s)",
                user["email"], user["name"])
        else:
            user_id = user["id"]
        self.set_secure_cookie("user", str(user_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

