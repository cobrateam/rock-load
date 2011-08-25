#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from tornado.web import authenticated

from rockload.apps.base.handlers import BaseHandler
from rockload.apps.main.models import Project, Test

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

class NewProjectHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('rockload/apps/main/new_project.html', errors=[], values={ 'name': '', 'gitrepo': '' })

    @authenticated
    def post(self):
        name = self.get_argument('name', '')
        git_repo = self.get_argument('gitrepo', '')

        errors = []
        if not name:
            errors.append('name')
        if not git_repo:
            errors.append('gitrepo')

        if errors:
            self.render('rockload/apps/main/new_project.html', errors=errors, values={ 'name': name, 'gitrepo': git_repo })
        else:
            prj = Project(name=name, git_repo=git_repo, created_at=datetime.now(), owner=self.get_current_user())
            prj.save()
            self.redirect('/projects/%s' % name)

class ProjectDetailsHandler(BaseHandler):
    @authenticated
    def get(self, project_name):
        all_projects = self.all_projects()
        project = Project.objects(name=project_name).get()
        tests = Test.objects(project=project).all()

        if tests:
            self.render('rockload/apps/main/project_details.html', projects=all_projects(), project=project, tests=tests)
        else:
            self.render('rockload/apps/main/no_tests.html', projects=all_projects(), project=project)

class NewTestHandler(BaseHandler):
    @authenticated
    def get(self, project_name):
        project = Project.objects(name=project_name).get()
        self.render('rockload/apps/main/new_test.html', projects=self.all_projects(), project=project,
                    errors=[], values={
                        'name': '',
                        'module': '',
                        'test_class': '',
                        'server_url': '',
                        'cycles': '',
                        'cycle_duration': ''
                    })
