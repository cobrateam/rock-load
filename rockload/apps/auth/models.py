#!/usr/bin/python
# -*- coding: utf-8 -*-

from mongoengine import Document, StringField

class User(Document):
    email = StringField(required=True)
    name = StringField(required=True)
