#!/usr/bin/python
# -*- coding: utf-8 -*-

from rockload.apps.main.handlers import IndexHandler, NoProjectsHandler, NewProjectHandler

urls = (
    (r'^/?', IndexHandler),
    (r'^/noprojects/?', NoProjectsHandler),
    (r'^/projects/new/?', NewProjectHandler),
)
