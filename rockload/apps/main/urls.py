#!/usr/bin/python
# -*- coding: utf-8 -*-

from rockload.apps.main.handlers import IndexHandler, NoProjectsHandler

urls = (
    (r'^/?', IndexHandler),
    (r'^/noprojects/?', NoProjectsHandler),
)
