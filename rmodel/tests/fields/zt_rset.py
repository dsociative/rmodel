# coding: utf8

from redis.client import Redis
from rmodel.fields.rset import rset
from rmodel.models.runit import RUnit
from unittest2.case import TestCase


class TestModel(RUnit):
    prefix = 'testmodel'
    root = True

    names = rset()


class Test(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.model = TestModel()
        self.field = self.model.names

    def test_default(self):
        self.assertEqual(self.field.data(), [])

    def test_append(self):
        self.field.append('name')
        self.assertEqual(self.field.data(), ['name'])
        self.field.append('thatever')
        self.assertEqual(self.field.data(), ['thatever', 'name'])

    def test_append_dublication(self):
        self.field.append('name')
        self.field.append('name')
        self.assertEqual(self.field.data(), ['name'])

    def test_pop_none(self):
        self.assertEqual(self.field.pop(), None)

    def test_pop(self):
        self.field.append('name')
        self.assertEqual(self.field.pop(), 'name')
        self.assertEqual(self.field.data(), [])

    def test_remove_null(self):
        self.assertEqual(self.field.remove('name'), 0)

    def test_remove(self):
        self.field.append('name')
        self.assertEqual(self.field.remove('name'), 1)
        self.assertEqual(self.field.data(), [])

    def test_len(self):
        self.assertEqual(len(self.field), 0)
        self.field.append('name')
        self.field.append('name')
        self.assertEqual(len(self.field), 1)
        self.field.append('name2')
        self.assertEqual(len(self.field), 2)
