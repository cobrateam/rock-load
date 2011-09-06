#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import loads
from os.path import exists, join
import os
import optparse
import time
from urllib import urlopen, urlencode
from uuid import uuid4
import shutil

from fabric.api import local, lcd, settings

DEFAULT_PORT = 3333
DEFAULT_IP = '0.0.0.0'


def main():
    parser = optparse.OptionParser(usage="rockload-client or type rockload-client -h (--help) for help", description=__doc__, version="0.1.0")
    parser.add_option("-p", "--port", type="int", dest="port", default=DEFAULT_PORT, help = "The port where rockload-server is [default: %default]." )
    parser.add_option("-i", "--host", dest="host", default=DEFAULT_IP, help = "The ip address of rockload-server [default: %default]." )

    (opt, args) = parser.parse_args()

    server_url = "http://%s:%s" % (opt.host, opt.port)

    while True:
        task_details = fetch(server_url, '/next-task')
        if 'task-details' in task_details:
            details = task_details['task-details']
            print 'found task - %s' % details['url']
            result = process_task(server_url, details)
            if not post_results(server_url, details, result).read() == 'OK':
                print 'Failed sending results to server for test %s' % details['result_id']
        time.sleep(5)

def update_data(server_url, task_details, cloned, in_progress):
    return urlopen('%s/update-results' % server_url, urlencode({
        'result_id': task_details['result_id'],
        'run_id': task_details['run_id'],
        'cloned': cloned,
        'in_progress': in_progress
    }))


def post_results(server_url, task_details, result):
    return urlopen('%s/post-results' % server_url, urlencode({
        'result_id': task_details['result_id'],
        'run_id': task_details['run_id'],
        'result': result
    }))

def cant_start_task(server_url, task_details):
    result = urlopen('%s/can-start/%s' % (server_url, task_details['result_id']))
    can_start = result.read() == 'True'

    return not can_start


def process_task(server_url, task_details):
    repo_id = download_from_git(task_details['git_repo'])
    update_data(server_url, task_details, True, False)

    while cant_start_task(server_url, task_details):
        print "waiting for server to allow starting task..."
        time.sleep(1)

    update_data(server_url, task_details, True, True)
    xml_text = ''

    bench_path = '/tmp/rockload/%s/bench' % repo_id
    with lcd(bench_path):
        with settings(warn_only=True):
            command = """fl-run-bench -u %(url)s -c %(cycles)s -D %(duration)s --simple-fetch %(test_module)s %(test_class)s""" % task_details
            local(command)
        xml_text = open(join(bench_path, 'funkload.xml')).read()

    shutil.rmtree('/tmp/rockload/%s' % repo_id)
    return xml_text


def download_from_git(git_repo):
    repo_id = uuid4()
    if not exists('/tmp/rockload'):
        os.makedirs('/tmp/rockload')
    local('git clone %s /tmp/rockload/%s' % (git_repo, repo_id))

    return repo_id


def fetch(server_url, url):
    result = urlopen(join(server_url.rstrip('/'), url.lstrip('/')))
    if result.getcode() != 200:
        print 'URL %s%s was not found!' % (server_url, url)
        return {}

    return loads(result.read())


if __name__ == '__main__':
    main()
