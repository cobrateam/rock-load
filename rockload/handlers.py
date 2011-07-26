#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import dumps

import tornado.web
import tornado.auth

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

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

class NewTestHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, project_id):
        user = self.get_current_user()
        project = self.db.get("SELECT * FROM project WHERE id = %s", int(project_id))
        if not project: raise tornado.web.HTTPError(404)
        self.render("new_test.html", user=user, project=project)

    @tornado.web.authenticated
    def post(self, project_id):
        user = self.get_current_user()
        project = self.db.get("SELECT * FROM project WHERE id = %s", int(project_id))
        if not project: raise tornado.web.HTTPError(404)

        title = self.get_argument("title")
        description = self.get_argument("description")
        repo = self.get_argument("repository")
        test_class = self.get_argument("testclass")

        test = {
            'userId': user.id,
            'projectId': project.id,
            'title': title,
            'description': description,
            'repo': repo,
            'testClass': test_class
        }

        test_json = dumps(test);
        test_id = self.db.execute("INSERT INTO test(project_id, test_data) VALUES(%s, %s)", project.id, test_json)
        test['testId'] = test_id
        test_json = dumps(test)
        self.redis.rpush('tests', test_json)

class NextTestHandler(BaseHandler):
    def get(self):
        element = self.redis.rpop('tests') or ''
        self.set_header("Content-Type", "application/json")
        self.write(element)

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

