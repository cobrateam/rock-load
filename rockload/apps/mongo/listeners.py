#!/usr/bin/python
# -*- coding: utf-8 -*-

from mongoengine import connect

def app_start_handler(bus, app):
    connect(app.settings['mongo_db'], host=app.settings['mongo_host'], port=app.settings['mongo_port'])

def listen(app):
    app.subscribe('app_started', app_start_handler)
