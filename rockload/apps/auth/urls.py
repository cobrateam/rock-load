#!/usr/bin/python
# -*- coding: utf-8 -*-

from rockload.apps.auth.handlers import LoginHandler

urls = (
    (r'/login/?', LoginHandler),
)
