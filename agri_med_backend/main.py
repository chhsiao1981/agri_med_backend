#!/usr/bin/env python
# -*- coding: utf-8 -*-

from agri_med_backend.constants import *

import gevent.monkey; gevent.monkey.patch_all()

from bottle import Bottle, request, response, route, run, post, get, static_file, redirect, HTTPError, view, template

import random
import math
import base64
import time
import ujson as json
import sys
import argparse
from beaker.middleware import SessionMiddleware

from agri_med_backend import cfg
from agri_med_backend import util
from agri_med_backend.http_handlers.upload_img_handler import upload_img_handler
from agri_med_backend.http_handlers.get_img_handler import get_img_handler
from agri_med_backend.http_handlers.upload_data_handler import upload_data_handler
from agri_med_backend.http_handlers.submit_handler import submit_handler

app = Bottle()


@app.get('/')
def dummy():
    return _process_result("1")

@app.get('/2')
def dummy2():
    response.set_header('Accept', '*')
    response.set_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', '*')
    response.content_type = 'application/json'
    return '{"path":"\/get_img?name=1471758150032b445c57fdbee4c8e831192a86132698ed99461d2","success":true}'


@app.post('/upload/data')
def upload_data():
    params = _process_params()
    result = upload_data_handler(params)
    cfg.logger.warning('result: %s', result)
    return _process_result(result)


@app.post('/upload/img')
def upload_img():
    params = _process_params()
    files = _process_files()
    result = upload_img_handler(params, files)
    cfg.logger.warning('result: %s', result)
    return _process_result(result)


@app.get('/get/img')
def get_img():
    params = _process_params()
    result = get_img_handler(params)
    return _process_mime_result('image/jpeg', result)


@app.post('/submit')
def submit():
    params = _process_params()
    result = submit_handler(params)
    return _process_result(result)


def _process_params():
    return dict(request.params)


def _process_json_request():
    return util.json_loads(_process_body_request())


def _process_body_request():
    f = request.body
    f.seek(0)
    return f.read()


def _process_files():
    files = request.files
    cfg.logger.warning('files: %s', files)
    for filename, each_file in files.iteritems():
        cfg.logger.warning('filename: %s each_file: %s', filename, each_file)
    return files


def _process_result(the_obj):
    response.set_header('Accept', '*')
    response.set_header(name="Access-Control-Allow-Origin", value=request.get_header("Origin","*"))
    if request.get_header("Origin",""):
        response.set_header(name="Access-Control-Allow-Credentials", value="true")
    response.set_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
    response.set_header('Access-Control-Allow-Methods', '*')
    response.content_type = 'application/json'
    result = util.json_dumps(the_obj)

    cfg.logger.warning('result: %s', result)

    return result


def _process_mime_result(content_type, content):
    response.set_header('Accept', '*')
    response.set_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', '*')
    response.content_type = content_type
    return content


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='agri_med_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-l', '--log_filename', type=str, default='', required=False, help="log filename")
    parser.add_argument('-p', '--port', type=str, required=True, help="port")

    args = parser.parse_args()

    return (S_OK, args)


def _main():
    global app

    (error_code, args) = parse_args()

    cfg.init({"port": args.port, "ini_filename": args.ini, 'log_filename': args.log_filename})

    '''
    session_opts = {
        'session.cookie_expires': True,
        'session.encrypt_key': cfg.config.get('session_encrypt_key', ''),
        'session.httponly': True,
        'session.timeout': cfg.config.get('session_expire_timestamp', SESSION_EXPIRE_TIMESTAMP),
        'session.type': 'cookie',
        'session.validate_key': True,
    }

    app = SessionMiddleware(app, session_opts)
    '''

    run(app, host='0.0.0.0', port=cfg.config.get('port'), server='gevent')


if __name__ == '__main__':
    _main()
