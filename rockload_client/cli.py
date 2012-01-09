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

import commands
import logging

DEFAULT_PORT = 3333
DEFAULT_IP = '0.0.0.0'
DEFAULT_LOG_PATH = '%s/logs' % (os.environ['HOME'])


def main():
    parser = optparse.OptionParser(usage="rockload-client or type rockload-client -h (--help) for help", description=__doc__, version="0.1.0")
    parser.add_option("-p", "--port", type="int", dest="port", default=DEFAULT_PORT, help = "The port where rockload-server is [default: %default]." )
    parser.add_option("-i", "--host", dest="host", default=DEFAULT_IP, help = "The ip address of rockload-server [default: %default]." )
    parser.add_option("-l", "--log-path", dest="log_path", default=DEFAULT_LOG_PATH, help = "The path for the rockload-client logs  [default: %default]." )

    (opt, args) = parser.parse_args()

    log_path = "%s/rock-cli-%s.log" % (opt.log_path, os.getpid())
    logging.basicConfig(filename=log_path,level=logging.DEBUG)
    
    server_url = "http://%s:%s" % (opt.host, opt.port)

    while True:
        task_details = fetch(server_url, '/next-task')
        if 'task-details' in task_details:
            details = task_details['task-details']
            logging.debug('found task - %s' % details['url'])
            result = process_task(server_url, details)
            if not post_results(server_url, details, result).read() == 'OK':
                logging.debug('Failed sending results to server for test %s' % details['result_id'])
            else:
                logging.debug('Posted! Now go take a look at your RockLoad server!')
        time.sleep(5)

def update_data(server_url, task_details, cloned, in_progress):
    return urlopen('%s/update-results' % server_url, urlencode({
        'result_id': task_details['result_id'],
        'run_id': task_details['run_id'],
        'cloned': cloned,
        'in_progress': in_progress
    }))


def post_results(server_url, task_details, result):
    logging.debug('Trying to post results')
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
        logging.debug("waiting for server to allow starting task...")
        time.sleep(1)
    
    xml_text = ''
    update_data(server_url, task_details, True, True)
    bench_path = '/tmp/rockload/%s/bench' % repo_id
    command = "cd %s; " % (bench_path) + "fl-run-bench -u %(url)s -c %(cycles)s -D %(duration)s --simple-fetch %(test_module)s %(test_class)s" % (task_details)
    logging.debug("Starting benchmark... go get a cup a coffee")
    output = commands.getoutput(command)
    logging.debug(output)
    
    xml_text = open(join(bench_path, 'funkload.xml')).read()
    logging.debug('Cleaning Temp folder')
    shutil.rmtree('/tmp/rockload/%s' % repo_id)
    return xml_text

def download_from_git(git_repo):
    repo_id = uuid4()
    if not exists('/tmp/rockload'):
        os.makedirs('/tmp/rockload')
    output = commands.getoutput('git clone %s /tmp/rockload/%s' % (git_repo, repo_id))
    logging.debug(output)
    return repo_id


def fetch(server_url, url):
    result = urlopen(join(server_url.rstrip('/'), url.lstrip('/')))
    if result.getcode() != 200:
        logging.debug('URL %s%s was not found!' % (server_url, url))
        return {}

    return loads(result.read())


if __name__ == '__main__':
    main()
