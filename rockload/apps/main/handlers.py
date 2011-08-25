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
        self.render('rockload/apps/main/index.html', projects=self.all_projects(), project=None)

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
                        'cycles': '30:60:90',
                        'cycle_duration': 10,
                        'number_of_workers': 3
                    })

    def is_valid_cycles(self, cycles):
        for cycle in cycles.split(':'):
            try:
                int(cycle)
            except ValueError:
                return False
        return True

    @authenticated
    def post(self, project_name):
        project = Project.objects(name=project_name).get()

        name = self.get_argument('name', '')
        module = self.get_argument('module', '')
        test_class = self.get_argument('test_class', '')
        server_url = self.get_argument('server_url', '')
        cycles = self.get_argument('cycles', '')
        try:
            cycle_duration = float(self.get_argument('cycle_duration', ''))
        except ValueError:
            cycle_duration = 0
        try:
            number_of_workers = int(self.get_argument('number_of_workers', ''))
        except ValueError:
            number_of_workers = 0

        errors = []

        if not name: errors.append('name')
        if not module: errors.append('module')
        if not test_class: errors.append('test_class')
        if not server_url: errors.append('server_url')
        if not cycles or not self.is_valid_cycles(cycles): errors.append('cycles')
        if cycle_duration <= 0: errors.append('cycle_duration')
        if number_of_workers <= 0: errors.append('number_of_workers')

        if errors:
            self.render('rockload/apps/main/new_test.html', projects=self.all_projects(), project=project,
                        errors=errors, values={
                            'name': name,
                            'module': module,
                            'test_class': test_class,
                            'server_url': server_url,
                            'cycles': cycles,
                            'cycle_duration': cycle_duration,
                            'number_of_workers': number_of_workers
                        })
        else:
            test = Test(project=project,
                        name=name,
                        module=module,
                        test_class=test_class,
                        server_url=server_url,
                        cycles=cycles,
                        cycle_duration=cycle_duration,
                        number_of_workers=number_of_workers,
                        created_at=datetime.now())
            test.save()
            self.redirect('/projects/%s/tests/%s' % (project.name, test.name))

class TestDetailsHandler(BaseHandler):
    @authenticated
    def get(self, project_name, test_name):
        project = Project.objects(name=project_name).get()
        test_details = Test.objects(project=project, name=test_name).get()
 
        self.render('rockload/apps/main/test_details.html', projects=self.all_projects(), project=project, test_details=test_details)


