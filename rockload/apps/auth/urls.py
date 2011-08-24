#!/usr/bin/python
# -*- coding: utf-8 -*-

from rockload.apps.auth.handlers import LoginHandler, GoogleLoginHandler

urls = (
    (r'/login/?', LoginHandler),
    (r'/login/google/?', GoogleLoginHandler),
)
