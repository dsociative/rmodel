#coding: utf8

from redis.client import Redis
from rmodel.cursor import Cursor
from rmodel.fields.rfield import rfield
from rmodel.models.runit import RUnit
from rmodel.sessions.rsession import RSession
from rmodel.tests.base_test import BaseTest
from unittest2.case import TestCase


class TestModel(RUnit):

    prefix = 'testmodel'
    root = True

    id = rfield(int)
    name = rfield(prefix='name')


class StoreModel(RUnit):

    prefix = 'storemodel'
    store = rfield(int)


class NestedModel(TestModel):

    prefix = 'nested'
    name = rfield()
    nested = StoreModel()

incr_value = 0


class rfield_with_onincr(rfield):

    def onincr(self, value):
        global incr_value
        return rfield.onincr(self, value + incr_value)


class ModelWithIncr(RUnit):

    root = True
    incr_field = rfield_with_onincr(int, 0)


class RUnitTest(BaseTest):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.model = TestModel(self.redis)

    def test_init(self):
        self.assertTrue(isinstance(self.model.cursor, Cursor))

    def test_incr(self):
        global incr_value

        model = ModelWithIncr(redis=self.redis)

        self.assertEqual(model.incr_field.get(), 0)
        model.incr_field += 1
        self.assertEqual(model.incr_field.get(), 1)

        incr_value = 13

        model.incr_field += 11
        self.assertEqual(model.incr_field.get(), 1 + 13 + 11)

        model.incr_field.set(10)

        self.assertEqual(model.incr_field.get(), 10)

    def test_simple(self):
        self.assertEqual(self.model.id.get(), None)
        self.assertEqual(self.model.name.get(), None)

        self.model.id.set(1)
        self.assertEqual(self.model.id.get(), 1)
        self.model.name.set('test_name')
        self.model = TestModel(redis=self.redis)

        self.assertEqual(self.model.id.get(), 1)
        self.assertEqual(self.model.name.get(), 'test_name')
        self.assertEqual(self.model.data(), {'id': 1, 'name': 'test_name'})

    def test_data(self):
        self.model.id.set(1)
        self.model.name.set('test_name')

        self.assertEqual(self.model.id.get(), 1)
        self.assertEqual(self.model.name.get(), 'test_name')

        self.assertEqual(self.model.data(), {'id': 1, 'name': 'test_name'})

    def test_nested_model(self):
        model = NestedModel(redis=self.redis)
        self.assertEqual(len(model.fields()), 3)
        model.nested.store.set(1)
        self.assertEqual(model.nested.store.get(), 1)
        self.assertDictEqual(model.data(), {'nested': {'store': 1},
                                            'id': None, 'name': None})

    def test_cross_model(self):
        one, two = (NestedModel(prefix=1, redis=self.redis),
                    NestedModel(prefix=2, redis=self.redis))
        self.assertEqual(one.cursor.key, '1')
        self.assertEqual(two.cursor.key, '2')

        one.id.set(1)
        two.id.set(2)
        self.assertEqual(one.id.get(), 1)
        self.assertEqual(two.id.get(), 2)

        self.assertEqual(one.nested.cursor.key, '1:nested')
        self.assertEqual(two.nested.cursor.key, '2:nested')
        one.nested.store.set(1)
        two.nested.store.set(2)
        self.assertNotEqual(one.nested.store, two.nested.store)
        self.assertEqual(one.nested.store.get(), 1)
        self.assertEqual(two.nested.store.get(), 2)

    def test_defaults(self):
        TestModel.defaults = {'id': 334, 'name': 'HELLO'}

        self.assertEqual(self.model.id.get(), 334)
        self.assertEqual(self.model.name.get(), 'HELLO')
        TestModel.defaults = False

    def test_session_remove(self):
        session = self.model._session = RSession()
        self.model.remove()
        self.eq(session.changes(), {self.model.prefix: None})


class RootDBInitTest(TestCase):

    def setUp(self):
        self.model = NestedModel
        self.model.root = True
        self.redis = Redis()
        self.model = self.model(redis=self.redis)

    def test_init(self):
        self.assertEqual(self.model.redis, self.redis)

    def test_field(self):
        self.assertEqual(self.model.name.redis, self.redis)

    def test_nested_init(self):
        self.assertEqual(self.model.nested.redis, self.redis)

    def test_nested_field(self):
        self.assertEqual(self.model.nested.store.redis, self.redis)

        