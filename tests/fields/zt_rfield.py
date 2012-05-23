#coding: utf8

from fields.rfield import rfield
from redis.client import Redis
from rmodel import RModel
from unittest.case import TestCase

class TModel(RModel):
    prefix = 'model'

    field = rfield(int, 0)

class FModel(RModel):

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




