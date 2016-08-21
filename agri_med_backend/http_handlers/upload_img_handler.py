# -*- coding: utf-8 -*-

import ujson as json
import pandas as pd
import numpy as np
import re
from wand.image import Image

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
        content = the_file.file.read()
        with Image(blob=content) as original:
            width, height = original.size
            if width >= 600:
                new_height = int(height * 600 / width)
                original.resize(width=600, height=new_height)
            converted = original.convert(format='png')
            with open(filename, 'w') as f:
                converted.save(f)
    except Exception as e:
        cfg.logger.error('unable to save: filename: %s e: %s', filename, e)

    path = '/get/img?name=%s' % (basename)

    return {'success': True, 'path': path}
