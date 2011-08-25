#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from rockload.apps.auth.models import User
from rockload.apps.main.models import Project

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None

        queryset = User.objects(email=user_id)
        if queryset.count() == 0:
            return None

        return queryset[0]

    def all_projects(self):
        return Project.objects().all()
