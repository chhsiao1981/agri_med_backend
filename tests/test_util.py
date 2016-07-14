# -*- coding: utf-8 -*-

from agri_med_backend.constants import *

import unittest
import logging

from agri_med_backend import util


class TestUtil(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_db_find_one(self):
        util.db_force_remove('test', {})
        util.db_insert('test', [{"test1": 1, 'test2': 2}])

        db_result = util.db_find_one('test', {"test1": 1})

        assert db_result.get('test2', 0) == 2
