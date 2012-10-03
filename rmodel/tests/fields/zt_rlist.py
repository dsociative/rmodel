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

    def test_remove(self):
        self.model.names.append('hello', 'test')
        self.model.names.remove('hello')
        self.assertEqual(self.model.names.data(), ['test'])
        self.model.names.remove('not_in_redis_key')
        self.assertEqual(self.model.names.data(), ['test'])

    def test_remove_similar(self):
        for _ in xrange(2):
            self.field.append('value')

        self.field.remove('value', 1)
        self.assertEqual(self.field.data(), ['value'])

    def test_by_index(self):
        self.assertEqual(self.field.by_index('hello'), None)
        self.field.append('hello')
        self.assertEqual(self.field.by_index(0), 'hello')
        self.field.append('next')
        self.assertEqual(self.field.by_index(1), 'next')
        self.field.append(2)
        self.assertEqual(self.field.by_index(2), 2)

    def test_trim(self):
        self.field.append(*xrange(10))
        self.field.trim(1, 12)
        self.assertEqual(self.field.data(), list(xrange(1, 10)))
        self.field.trim(0, 0)
        self.assertEqual(self.field.data(), [1])

    def test_contains_false(self):
        self.assertEqual('hello' in self.model.names, False)

    def test_contains_true(self):
        self.model.names.append('hello')
        self.assertEqual('hello' in self.model.names, True)
