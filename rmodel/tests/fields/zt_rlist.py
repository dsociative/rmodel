#coding: utf8

from redis.client import Redis
from rmodel.fields.rfield import rfield
from rmodel.fields.rlist import rlist
from rmodel.models.runit import RUnit
from unittest2.case import TestCase


class TestModel(RUnit):

    prefix = 'testmodel'
    root = True

    id = rfield(int)
    names = rlist()


class TypingModel(RUnit):

    root = True
    names = rlist(int)


class Test(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.model = TestModel()
        self.field = self.model.names

    def test_(self):
        self.assertEqual(self.model.names.data(), [])
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

    def test_set(self):
        self.field.set(['123', '42'])
        self.assertEqual(self.field.data(), [123, 42])

    def test_typing(self):
        model = TypingModel()
        model.names.set(['123', '42'])

        self.assertEqual(model.data(), {'names': [123, 42]})
        self.assertEqual(model.names.data(), [123, 42])
