#!/usr/bin/python
# -*- coding: utf-8 -*-

from mongoengine import Document, StringField, ReferenceField, DateTimeField, FloatField, IntField

from rockload.apps.auth.models import User

class Project(Document):
    owner = ReferenceField(User, required=True)
    created_at = DateTimeField(required=True)
    name = StringField(required=True, unique=True)
    git_repo = StringField(required=True)

    @classmethod
    def get_projects_for_user(cls, user):
        return cls.objects(owner=user).all()

    @property
    def tests(self):
        return Test.objects(project=self).all()

class Test(Document):
    project = ReferenceField(Project, required=True)
    created_at = DateTimeField(required=True)
    name = StringField(required=True, unique=True)
    module = StringField(required=True)
    test_class = StringField(required=True)
    server_url = StringField(required=True)
    cycles = StringField(required=True, default="30:60:90")
    cycle_duration = FloatField(required=True, default=10.0)
    number_of_workers = IntField(required=True, default=3)

    @property
    def runs(self):
        return TestRun.objects(test=self).all()

class TestRun(Document):
    test = ReferenceField(Test, required=True)
