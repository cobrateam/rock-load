#!/usr/bin/python
# -*- coding: utf-8 -*-

from rockload.apps.main.handlers import IndexHandler, NoProjectsHandler, NewProjectHandler,\
                            ProjectDetailsHandler, NewTestHandler, TestDetailsHandler,\
                            StartTestHandler, NextTaskHandler, SaveResultsHandler

urls = (
    (r'^/?', IndexHandler),
    (r'^/noprojects/?', NoProjectsHandler),
    (r'^/next-task/?', NextTaskHandler),
    (r'^/post-results/?', SaveResultsHandler),
    (r'^/projects/new/?', NewProjectHandler),
    (r'^/projects/([^/]+)/tests/new/?', NewTestHandler),
    (r'^/projects/([^/]+)/tests/(.+?)/start?', StartTestHandler),
    (r'^/projects/([^/]+)/tests/(.+?)/?', TestDetailsHandler),
    (r'^/projects/(.+?)/?', ProjectDetailsHandler),
)
