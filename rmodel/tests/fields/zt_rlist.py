#coding: utf8

from redis.client import Redis
from rmodel.fields.rfield import rfield
from rmodel.fields.rlist import rlist
from rmodel.models.runit import RUnit
from unittest.case import TestCase


class TestModel(RUnit):

    prefix = 'testmodel'
    root = True

    id = rfield(int)
    names = rlist()


class Test(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.model = TestModel()
        self.field = self.model.names

    def test_(self):
        self.assertEqual(self.model.names.default, [])
        self.assertEqual(self.model.data(), {'id': None, 'names': []})

        self.assertEqual(len(self.field), 0)
        self.field.append('myname')
        self.assertEqual(self.field.data(), ['myname'])
        self.field.append('sd')
        self.assertEqual(self.field.data(), ['myname', 'sd'])
        self.assertEqual(len(self.field), 2)
        self.field.append('one', 'two')
        self.assertEqual(self.field.data(), ['myname', 'sd', 'one', 'two'])

    def test_pop(self):
        self.assertEqual(self.field.data(), [])
        self.field.append('value1')
        self.assertEqual(self.field.data(), ['value1'])
        self.assertEqual(self.field.pop(), 'value1')
        self.assertEqual(self.field.pop(), None)






