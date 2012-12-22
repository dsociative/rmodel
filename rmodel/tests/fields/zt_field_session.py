# -*- coding: utf8 -*-
from rmodel.sessions.rsession import RSession
from rmodel.tests.base_test import BaseTest


class FieldSessionTest(BaseTest):

    def setUp(self):
        super(FieldSessionTest, self).setUp()
        self.session = self.field._session = RSession()