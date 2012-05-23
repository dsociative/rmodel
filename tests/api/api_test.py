# coding: utf8

from model.tests.api.zt_db import TDB
from unittest.case import TestCase

class ApiTest(TestCase):

    def setUp(self):

        self.model = TDB()

        self.redis = self.model.redis
        self.redis.flushdb()

        for i in xrange(33):
            self.model.set(i).id = i

        self.item = self.model.set(55)
        self.item.id = 55
        self.item.deep.value = 'something special'

    def test_data(self):
        out = self.model.api('prefix=55')
        self.assertEqual(out, [self.item.data()])


        out = self.model.api('deep.value=something special')
        self.assertEqual(out, [self.item.data()])


    def test_action(self):
        self.model.api('prefix=55 set value=qwerty')
        self.assertEqual(self.item.value, 'qwerty')


        self.model.api('deep.value=something special set deep.value=qwerty')
        self.assertEqual(self.item.deep.value, 'qwerty')
