# -*- coding: utf-8 -*-

import ujson as json
import pandas as pd
import numpy as np
import re

from agri_med_backend.constants import *
from agri_med_backend import cfg
from agri_med_backend import util


def upload_img_handler(params, files):
    cfg.logger.warning('params: %s files: %s', params, files)

    the_file = files.get('file', None)
    if not the_file:
        return {'success': False, 'errorMsg': 'no file'}

    basename = ''
    the_timestamp = util.get_timestamp()
    while True:
        basename = str(the_timestamp) + util.gen_random_string()
        if basename[0] != '-':
            break

    filename = cfg.config.get('img_dir', '/data/agri_med/img') + '/' + basename

    cfg.logger.warning('to write file: the_file: %s name: %s basename: %s filename: %s', the_file, the_file.name, basename, filename)
    try:
        the_file.save(filename)
    except Exception as e:
        cfg.logger.error('unable to save: filename: %s e: %s', filename, e)

    path = '/get/img?name=%s' % (basename)

    return {'success': True, 'path': path}
