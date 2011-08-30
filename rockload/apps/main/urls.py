#!/usr/bin/python
# -*- coding: utf-8 -*-

from rockload.apps.main.handlers import IndexHandler, NoProjectsHandler, NewProjectHandler
from rockload.apps.main.handlers import ProjectDetailsHandler, NewTestHandler, TestDetailsHandler
from rockload.apps.main.handlers import StartTestHandler

urls = (
    (r'^/?', IndexHandler),
    (r'^/noprojects/?', NoProjectsHandler),
    (r'^/projects/new/?', NewProjectHandler),
    (r'^/projects/([^/]+)/tests/new/?', NewTestHandler),
    (r'^/projects/([^/]+)/tests/(.+?)/start?', StartTestHandler),
    (r'^/projects/([^/]+)/tests/(.+?)/?', TestDetailsHandler),
    (r'^/projects/(.+?)/?', ProjectDetailsHandler),
)
