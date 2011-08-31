#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import quote

from mongoengine import EmbeddedDocument, Document, StringField, ReferenceField, DateTimeField, FloatField, IntField
from mongoengine import EmbeddedDocumentField, ListField

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

    @property
    def url(self):
        return "/projects/%s" % quote(self.name)


class TestStats(EmbeddedDocument):
    number_of_tests = IntField(required=True, default=0)
    total_testing_duration = IntField(required=True, default=0)
    avg_reqs_sec = FloatField(required=True, default=0.0)
    avg_response_time = FloatField(required=True, default=0.0)

    @property
    def total_duration(self):
        seconds = int(self.total_testing_duration)
        hours = seconds / 3600
        seconds -= 3600*hours
        minutes = seconds / 60
        seconds -= 60*minutes
        if hours == 0:
            return "%02d:%02d" % (minutes, seconds)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)


class Test(Document):
    project = ReferenceField(Project, required=True)
    created_at = DateTimeField(required=True)
    name = StringField(required=True, unique=True)

    module = StringField(required=True)
    test_class = StringField(required=True)
    server_url = StringField(required=True)
    cycles = StringField(required=True, default="30:60:90")
    cycle_duration = IntField(required=True, default=10)
    number_of_workers = IntField(required=True, default=3)

    stats = EmbeddedDocumentField(TestStats)

    @property
    def runs(self):
        return [result for result in TestResult.objects(test=self).all() if result.done]

    @property
    def url(self):
        return "/projects/%s/tests/%s" % (quote(self.project.name), quote(self.name))


class TestRun(EmbeddedDocument):
    uuid = StringField(required=True)
    git_repo = StringField(required=True)
    module = StringField(required=True)
    test_class = StringField(required=True)
    server_url = StringField(required=True)
    cycles = StringField(required=True)
    cycle_duration = IntField(required=True)
    xml = StringField(required=False)


class TestResult(Document):
    test = ReferenceField(Test, required=True)
    number_of_workers = IntField(required=True)
    html_path = StringField(required=False)
    duration_in_seconds = IntField(required=False)
    date = DateTimeField(required=False)
    runs = ListField(EmbeddedDocumentField(TestRun))

    @property
    def done(self):
        for run in self.runs:
            if not run.xml:
                return False
        return True

    @property
    def formatted_date(self):
        return self.date.strftime('%d/%m/%Y %H:%M:%S')
