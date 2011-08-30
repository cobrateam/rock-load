#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import loads
from os.path import exists, join
import os
import optparse
import time
from urllib import urlopen, urlencode
from uuid import uuid4
import glob

from fabric.api import local, lcd

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
            result = process_task(details)
            if not post_results(server_url, details, result).getcode() == '200':
                print 'Failed sending results to server for test %s' % details['result_id']
        time.sleep(2)

def post_results(server_url, task_details, result):
    return urlopen('%s/post-results' % server_url, urlencode({
        'result_id': task_details['result_id'],
        'result': result
    }))

def process_task(task_details):
    repo_id = download_from_git(task_details['git_repo'])

    xml_text = ''

    bench_path = '/tmp/rockload/%s/bench' % repo_id
    with lcd(bench_path):
        command = """fl-run-bench -u %(url)s -c %(cycles)s -D %(duration)s --simple-fetch %(test_module)s %(test_class)s""" % task_details
        local(command)
        xml_text = open(join(bench_path, 'funkload.xml')).read()

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
