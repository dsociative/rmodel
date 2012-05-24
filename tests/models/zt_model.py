#coding: utf8

from cursor import Cursor
from fields.rfield import rfield
from redis.client import Redis
from rmodel import RModel
from unittest.case import TestCase

class TestModel(RModel):

    prefix = 'testmodel'

    id = rfield(int)
    name = rfield(prefix='name')

class StoreModel(RModel):

    prefix = 'storemodel'
    store = rfield(int)

class NestedModel(TestModel):

    prefix = 'nested'

    nested = StoreModel()

incr_value = 0

class rfield_with_onincr(rfield):

    def onincr(self, value):
        global incr_value
        return rfield.onincr(self, value + incr_value)


class ModelWithIncr(RModel):

    incr_field = rfield_with_onincr(int, 0)

class Test(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()

    def test_init(self):
        model = TestModel()
        self.assertTrue(isinstance(model.cursor, Cursor))

    def test_incr(self):
        global incr_value

        model = ModelWithIncr()
        model.id = 0

        self.assertEqual(model.incr_field.get(), 0)
        model.incr_field += 1
        self.assertEqual(model.incr_field.get(), 1)

        incr_value = 13

        model.incr_field += 11
        self.assertEqual(model.incr_field.get(), 1 + 13 + 11)

        model.incr_field.set(10)

        self.assertEqual(model.incr_field.get(), 10)

    def test_simple(self):
        model = TestModel()

        self.assertEqual(model.id.get(), None)
        self.assertEqual(model.name.get(), None)

        model.id.set(1)
        self.assertEqual(model.id.get(), 1)
        model.name.set('test_name')
        model = TestModel()

        self.assertEqual(model.id.get(), 1)
        self.assertEqual(model.name.get(), 'test_name')
        model['qwe'] = 1
        self.assertEqual(model.data(), {'id': 1, 'name': 'test_name'})

    def test_data(self):
        model = TestModel()

        model.id.set(1)
        model.name.set('test_name')

        self.assertEqual(model.id.get(), 1)
        self.assertEqual(model.name.get(), 'test_name')

        self.assertEqual(model.data(), {'id':1, 'name':'test_name'})

    def test_nested_model(self):
        model = NestedModel()
        self.assertEqual(id(model.nested.instance), id(model))

        self.assertEqual(len(model.fields), 3)
        model.nested.store.set(1)
        self.assertEqual(model.nested.store.get(), 1)
        self.assertDictEqual(model.data(),
                         {'nested': {'store':1},
                          'id': None, 'name': None})

    def test_cross_model(self):
        one, two = NestedModel(prefix=1), NestedModel(prefix=2)
        self.assertEqual(one.cursor.key, '1')
        self.assertEqual(two.cursor.key, '2')

        one.id.set(1)
        two.id.set(2)
        self.assertEqual(one.id.get(), 1)
        self.assertEqual(two.id.get(), 2)

        one.nested.store.set(1)
        two.nested.store.set(2)
        self.assertEqual(one.nested.store.get(), 1)
        self.assertEqual(two.nested.store.get(), 2)

    def test_defaults(self):
        model = TestModel()
        TestModel.defaults = {'id':334, 'name':'HELLO'}

        self.assertEqual(model.id.get(), 334)
        self.assertEqual(model.name.get(), 'HELLO')
        TestModel.defaults = False



