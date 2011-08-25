#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.web import authenticated

from rockload.apps.base.handlers import BaseHandler
from rockload.apps.main.models import Project

class IndexHandler(BaseHandler):
    @authenticated
    def get(self):
        if not Project.get_projects_for_user(self.get_current_user()):
            self.redirect("/noprojects")
        self.render('rockload/apps/main/index.html')

class NoProjectsHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('rockload/apps/main/no_projects.html')
