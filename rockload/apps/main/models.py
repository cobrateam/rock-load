#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import quote
from os.path import join, exists
from lxml import etree

from mongoengine import EmbeddedDocument, Document, StringField, ReferenceField, DateTimeField, FloatField, IntField
from mongoengine import EmbeddedDocumentField, ListField, BooleanField

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
    number_of_requests = IntField(required=True, default=0)
    total_request_duration = FloatField(required=True, default=0.0)
    avg_reqs_sec = FloatField(required=True, default=0.0)
    avg_response_time = FloatField(required=True, default=0.0)

    @property
    def total_duration(self):
        seconds = int(self.total_request_duration)
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

    def update_stats(self):
        results = self.runs

        number_of_requests = 0
        total_request_duration = 0.0
        avg_reqs_sec = 0.0
        avg_response_time = 0.0

        for result in results:
            number_of_requests += result.stats.number_of_requests
            total_request_duration += result.stats.total_request_duration
            avg_reqs_sec += result.stats.avg_reqs_sec
            avg_response_time += result.stats.avg_response_time

        avg_response_time = avg_response_time / len(results)
        avg_reqs_sec = avg_reqs_sec / len(results)

        self.stats.number_of_requests = number_of_requests
        self.stats.total_request_duration = total_request_duration
        self.stats.avg_reqs_sec = avg_reqs_sec
        self.stats.avg_response_time = avg_response_time
        self.save()

class TestRun(EmbeddedDocument):
    uuid = StringField(required=True)
    git_repo = StringField(required=True)
    module = StringField(required=True)
    test_class = StringField(required=True)
    server_url = StringField(required=True)
    cycles = StringField(required=True)
    cycle_duration = IntField(required=True)
    xml = StringField(required=False)
    in_progress = BooleanField(required=True, default=False)


class TestResult(Document):
    test = ReferenceField(Test, required=True)
    number_of_workers = IntField(required=True)
    html_path = StringField(required=False)
    duration_in_seconds = IntField(required=False)
    date = DateTimeField(required=False)
    runs = ListField(EmbeddedDocumentField(TestRun))

    stats = EmbeddedDocumentField(TestStats)

    def update_stats(self, report_dir):
        if not self.html_path: return
        html_file = join(report_dir.rstrip('/'), self.html_path.lstrip('/'))
        if not exists(html_file): return

        parser = etree.HTMLParser()
        html = etree.parse(open(html_file, 'rb'), parser)

        table_xpath = "//div[@id='funkload-bench-report']/div[@id='request-stats']//table[@class='docutils']//tr/td[%(column)d]"

        requests_per_second = html.xpath(table_xpath % { 'column': 4 })
        average_request_times = html.xpath(table_xpath % { 'column': 10 })
        total_requests = html.xpath(table_xpath % { 'column': 6 })

        def sum_collection(coll):
            return reduce(lambda accumulator, item: accumulator + float(item.text), coll, 0.0)

        sum_rps = sum_collection(requests_per_second)
        sum_rt = sum_collection(average_request_times)
        number_of_requests = sum_collection(total_requests)

        self.stats.number_of_requests = number_of_requests
        self.stats.avg_reqs_sec = sum_rps / len(requests_per_second)
        self.stats.avg_response_time = sum_rt / len(average_request_times)
        self.stats.total_request_duration = self.stats.avg_response_time * self.stats.number_of_requests

        self.save()

    @property
    def done(self):
        for run in self.runs:
            if not run.xml:
                return False
        return True

    @property
    def formatted_date(self):
        if not self.date: return ''
        return self.date.strftime('%d/%m/%Y %H:%M:%S')


