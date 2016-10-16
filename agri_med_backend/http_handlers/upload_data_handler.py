# -*- coding: utf-8 -*-

import ujson as json
import pandas as pd
import numpy as np
import re
import smtplib
import email
from email.mime.text import MIMEText
from jinja2 import Template
import pdfkit
import urllib

from agri_med_backend.constants import *
from agri_med_backend import cfg
from agri_med_backend import util


def upload_data_handler(params):
    # 名字
    name = params.get('name', '')

    # 地址
    address = params.get('address', '')

    # email
    email_address = params.get('email', '')

    # 作物
    crop = params.get('crop', '')

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

    content, filename = _format_email(name, address, email_address, crop, variety, before, day, sick_day, acre, sick_acre, comment, whole_view, single_view, feature_view, root_view)

    error = _send_email(content, filename, email_address)
    if error:
        return {'success': False, 'errorMsg': error}

    return {'success': True, 'errorMsg': ''}


def _format_email(name, address, email_address, crop, variety, before, day, sick_day, acre, sick_acre, comment, whole_view, single_view, feature_view, root_view):
    with open('templates/template.html', 'r') as f:
        the_template = Template(f.read())

    the_map = {
        'name': name,
        'address': address,
        'email': email_address,
        'crop': crop,
        'variety': variety,
        'before': before,
        'day': day,
        'sick_day': sick_day,
        'acre': acre,
        'sick_acre': sick_acre,
        'comment': comment,
        'whole_view': whole_view,
        'single_view': single_view,
        'feature_view': feature_view,
        'root_view': root_view,
    }

    content = the_template.render(the_map).strip()

    filename = cfg.config.get('pdf_dir', '/data/agri_med/pdf') + '/' + util.gen_random_string() + '.pdf'

    pdfkit.from_string(content, filename)

    return content, filename


def _send_email(content, filename, email_address):
    if not content:
        return None

    error = None

    title = '[醫農] 您所回報的植物病蟲害資訊已準備好了'

    msg['From'] = 'noreply@roadpin.tw'
    msg['To'] = email_address
    msg['Subject'] = title

    file_msg = email.mime.base.MIMEBase('image', 'png')

    try:
        s = smtplib.SMTP(cfg.config.get('error_smtp_host', 'msa.hinet.net'))
        s.sendmail(msg['From'], cfg.config.get(mail_list_cfg, ['chhsiao@appier.com']), msg.as_string())
        s.quit()
    except Exception as e:
        error = Error(S_ERR, 'failed to send email: e: %s' % (e))
        cfg.logger.error(error)

    return error
