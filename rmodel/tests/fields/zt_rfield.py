#coding: utf8

from redis.client import Redis
from rmodel.fields.rfield import rfield
from rmodel.models.runit import RUnit
from unittest2.case import TestCase


class TModel(RUnit):
    prefix = 'model'
    root = True

    field = rfield(int, 0)


class FModel(RUnit):

    prefix = 'model'


class RfieldTest(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.model = TModel()

    def test_init(self):
        self.assertEqual(self.model.field.get(), 0)
        self.assertEqual(self.model.field._changes, None)

    def test_incr(self):
        self.model.field -= 10
        self.assertEqual(self.model.field.get(), -10)

    def test_changes_set(self):
        self.model.field.set('123')
        self.assertEqual(self.model.field.changes(), '123')

    def test_changes_clean(self):
        self.model.field.set('123')
        self.model.field.clean()
        self.assertEqual(self.model.field.changes(), None)
