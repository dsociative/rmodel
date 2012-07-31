#coding: utf8

from redis.client import Redis
from rmodel.fields.rfield import rfield
from rmodel.models.runit import RUnit
from unittest.case import TestCase


class TModel(RUnit):
    prefix = 'model'
    root = True

    field = rfield(int, 0)


class FModel(RUnit):

    prefix = 'model'


class Test(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()

    def test_init(self):
        model = TModel()

        self.assertEqual(model.field.get(), 0)
        model.field -= 10
        self.assertEqual(model.field.get(), -10)

    def test_changes(self):
        model = TModel()
        self.assertEqual(model.field._changes, None)
        model.field.set('123')
        self.assertEqual(model.field._changes, '123')

