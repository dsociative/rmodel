# coding: utf8

from model.rmodel import RModel
from model.rmodel_store import RModelStore
from redis.client import Redis
from unittest.case import TestCase
from model.fields.rinmodel import rinmodel


class Build(RModel):

    x = rinmodel(int, 0)
    y = rinmodel(int, 0)


class Buildings(RModelStore):

    prefix = 'testmodel'
    assign = Build


class Item(RModel):

    names = rinmodel(int, 0)
    names2 = rinmodel()

    buildings = Buildings


class StoreModel(RModelStore):

    prefix = 'testmodel'
    assign = Item


class TestInModelField(TestCase):
    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()

        self.model = StoreModel()
        self.item1 = self.model.set(1)
        self.item2 = self.model.set(2)

        self.item1.names.set(1)
        self.item1.names2.set(2)
        self.item2.names.set(3)
        self.item2.names2.set(4)

    def test_keys(self):

        self.item1.names.clean()
        self.assertEqual(self.item1.names.get(), 0)
        self.item1.names.set(123)
        self.assertEqual(self.item1.names.get(), 123)

        self.item1.names2.clean()
        self.assertEqual(self.item1.names2.get(), None)
        self.item1.names2.set(700)
        self.assertEqual(self.item1.names2.get(), '700')
        self.assertEqual(self.item1.names.get(), 123)

        self.item2.names2.set(200)
        self.item2.names.set(100)
        self.assertEqual(self.item1.names2.get(), '700')
        self.assertEqual(self.item1.names.get(), 123)
        self.assertEqual(self.item2.names2.get(), '200')
        self.assertEqual(self.item2.names.get(), 100)

        self.assertEqual(self.item1.cursor.key, 'testmodel:1')
        self.assertEqual(self.item2.cursor.key, 'testmodel:2')

        self.assertEqual(self.item1.names.key, 'testmodel:data')
        self.assertEqual(self.item1.names2.key, 'testmodel:data')
        self.assertEqual(self.item2.names.key, 'testmodel:data')
        self.assertEqual(self.item2.names2.key, 'testmodel:data')

        self.assertEqual(self.redis.hgetall('testmodel:data'),
                                {'1@names': '123', '1@names2': '700',
                                 '2@names': '100', '2@names2': '200'})

    def test_remove(self):
        self.model.remove_item(1)
        self.assertEqual(self.redis.hgetall('testmodel:data'),
                                {'2@names': '3', '2@names2': '4'})
        self.model.remove_item(2)
        self.assertEqual(self.redis.hgetall('testmodel:data'), {})

    def test_clean(self):
        self.item1.names.clean()
        self.assertEqual(self.redis.hgetall('testmodel:data'), {'1@names2': '2',
                                                                 '2@names': '3',
                                                                 '2@names2': '4'})

        self.item1.names2.clean()
        self.assertEqual(self.redis.hgetall('testmodel:data'), {'2@names': '3',
                                                                 '2@names2': '4'})

        self.item2.names.clean()
        self.assertEqual(self.redis.hgetall('testmodel:data'), {'2@names2': '4'})

        self.item2.names2.clean()
        self.assertEqual(self.redis.hgetall('testmodel:data'), {})

    def test_include(self):
        build1 = self.item1.buildings.set(1)
        build2 = self.item1.buildings.set(2)

        key = 'testmodel:1:buildings:data'

        self.assertEqual(build1.x.key, key)
        self.assertEqual(build2.x.key, key)
        self.assertEqual(build1.y.key, key)
        self.assertEqual(build2.y.key, key)

        build1.x.set(1)
        build1.y.set(2)
        build2.x.set(3)
        build2.y.set(4)

        self.assertEqual(self.redis.hgetall(key), {'2@y': '4', '2@x': '3',
                                                   '1@x': '1', '1@y': '2'})

        build1.x.clean()
        self.assertEqual(self.redis.hgetall(key), {'2@y': '4', '2@x': '3',
                                                   '1@y': '2'})

        self.item1.buildings.remove_item(2)
        self.assertEqual(self.redis.hgetall(key), {'1@y': '2'})

        build1.y.clean()
        self.assertEqual(self.redis.hgetall(key), {})
