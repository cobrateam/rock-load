#!/usr/bin/python
# -*- coding: utf-8 -*-

from mongoengine import connect

def app_start_handler(app):
    connect('rockload', host='localhost', port=12345)

def listen(app):
    app.subscribe('app_started', app_start_handler)
