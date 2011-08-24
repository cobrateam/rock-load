#!/usr/bin/python
# -*- coding: utf-8 -*-

from rockload.apps.main.handlers import IndexHandler

urls = (
    (r'^/?', IndexHandler),
)
