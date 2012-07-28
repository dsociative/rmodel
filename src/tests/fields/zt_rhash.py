#coding: utf8

from fields.rhash import rhash
from fields.unbound import Unbound
from redis.client import Redis
from rmodel import RModel
from unittest.case import TestCase


class TModel(RModel):
    prefix = 'model'
    root = True
    hash = rhash(int)


class FModel(RModel):
    root = True
    prefix = 'model'


class Test(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()

    def test_init(self):
        model = TModel()

        unbound_field = rhash(int, 0)
        self.assertIsInstance(rhash('test', int, 0), Unbound)

        self.assertIsInstance(unbound_field, Unbound)
        bound_field = unbound_field.bound(model, 'test')

        self.assertIsInstance(bound_field, rhash)
        self.assertIsInstance(rhash('test', int, 0), Unbound)

        bound_field['q'] = 1
        self.assertEqual(bound_field.data(), {'q': 1})
        self.assertEqual(bound_field.prefix, 'test')

    def test_two_model(self):
        model1 = TModel(prefix='1')
        model2 = TModel(prefix='2')

        model2.hash['1'] = 1

        self.assertDictEqual(model1.data(), {'hash':{}})
        self.assertDictEqual(model2.data(), {'hash':{'1': 1}})




