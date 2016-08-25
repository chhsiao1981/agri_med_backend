# -*- coding: utf-8 -*-

import ujson as json
import pandas as pd
import numpy as np
import re
import smtplib
from email.mime.text import MIMEText
from jinja2 import Template

from agri_med_backend.constants import *
from agri_med_backend import cfg
from agri_med_backend import util


def upload_data_handler(params):
    # 名字
    name = params.get('name', '')

    # 地址
    address = params.get('address', '')

    # email
    email = params.get('email', '')

    # 作物
    crop = params.('crop', '')

    # 品種
    variety = params.get('variety', '')

    # 前期作物
    before = params.get('before', '')

    # 種植天數
    day = params.get('day', '')

    # 發病天數
    sick_day = params.get('sickDay', '')

    # 種植面積
    acre = params.get('acre', '')

    # 發病面積
    sick_acre = params.get('sickAcre', '')

    # 補充說明
    comment = params.get('comment', '')

    # 全景
    whole_view = params.get('wholeView', [])

    # 單株
    single_view = params.get('singleView', [])

    # 患部
    feature_view = params.get('featureView', [])

    # 根部
    root_view = params.get('rootView', [])

    content, files = _format_email(name, address, email, crop, variety, before, day, sick_day, acre, sick_acre, comment, whole_view, single_view, feature_view, root_view)

    error = _send_email(content, files)
    if error:
        return {'success': False, 'errorMsg': error}

    return {'success': True, 'errorMsg': ''}


def _format_email(name, address, email, crop, variety, before, day, sick_day, acre, sick_acre, comment, whole_view, single_view, feature_view, root_view):
    with open('templates/template.html', 'r') as f:
        the_template = Template(f.read())

    content = the_template.render(the_map).strip()

    return content, []


def _send_email(content, files, email):
    if not content:
        return None

    error = None

    title = '[醫農] 您所回報的植物病蟲害資訊已準備好了'

    msg = MIMEText(str(text))
    msg['From'] = 'noreply@roadpin.tw'
    msg['To'] = email
    msg['Subject'] = title

    try:
        s = smtplib.SMTP(cfg.config.get('error_smtp_host', 'msa.hinet.net'))
        s.sendmail(msg['From'], cfg.config.get(mail_list_cfg, ['chhsiao@appier.com']), msg.as_string())
        s.quit()
    except Exception as e:
        error = Error(S_ERR, 'failed to send email: e: %s' % (e))
        cfg.logger.error(error)

    return error
