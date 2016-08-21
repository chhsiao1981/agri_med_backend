# -*- coding: utf-8 -*-

import ujson as json
import pandas as pd
import numpy as np
import re

from agri_med_backend.constants import *
from agri_med_backend import cfg
from agri_med_backend import util


def get_img_handler(params):
    basename = params.get('name', '')
    filename = cfg.config.get('img_dir', '/data/agri_med/img') + '/' + basename

    with open(filename, 'r' ) as f:
        content = f.read()

    return content
