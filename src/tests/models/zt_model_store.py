# coding: utf8

from fields.rfield import rfield
from fields.rhash import rhash
from redis.client import Redis
from rmodel import RModel
from rmodel_store import RModelStore
from unittest.case import TestCase


class ItemModel(RModel):

    id = rfield(int)
    total = rfield(int)
    hash = rhash(int, 0)


class StoreModel(RModelStore):

    assign = ItemModel

    prefix = 'store'
    name = rfield(str, 'default_name')


class IndexModel(RModel):

    prefix = 'model'
    root = True

    lenght = rfield()
    store = StoreModel()


class RModelStoreTest(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()

    def test_init(self):
        model = IndexModel()
        self.assertIsInstance(model, IndexModel)

    def test_addModel(self):
        model = IndexModel()
        item = model.store.add()
        self.assertEqual(isinstance(item, ItemModel), True)

        item.id.set(1)
        item.total.set(1)
        data = item.data()

        self.assertEqual(data, {'id': 1, 'hash': {}, 'total': 1})
        self.assertEqual(model.store.keys(), ['1'])
        self.assertEqual(1 in model.store, True)
        self.assertEqual(len(model.store), 1)

        self.assertEqual(model.store.get(1).data(), data)

        self.assertEqual(model.store.new_key(), long(2))
        item = model.store.add()
        self.assertEqual(model.store.new_key(), long(4))
        self.assertEqual(len(model.store), 2)

    def test_data(self):
        model = IndexModel()
        item = model.store.add()
        self.assertEqual(isinstance(item, ItemModel), True)
        item.total.set(2)
        item.id.set(1)

        item2 = model.store.set(2)
        item2.id.set(8)
        item2.total.set(4)
        self.assertEqual(item.id.get(), 1)
        self.assertEqual(item.total.get(), 2)

        self.assertDictEqual(item.data(), {'total': 2, 'hash':{}, 'id': 1})
        self.assertDictEqual(item2.data(), {'total': 4, 'hash':{}, 'id': 8})
        self.assertDictEqual(model.store.data(),
                         {'1': {'hash': {}, 'id': 1, 'total': 2},
                          '2': {'hash': {}, 'id': 8, 'total': 4},
                          'name': 'default_name'})

    def test_remove(self):
        model = IndexModel()
        item = model.store.add()
        item.total = 2
        item.id = 1

        self.assertTrue(model.store.get(1))
        model.store.remove_item(1)
        self.assertFalse(model.store.get(1))

    def test_with_model(self):
        model = StoreModel(inst=None)
        self.assertEqual(model.data(), {'name': 'default_name'})

    def test_two_models(self):
        model = StoreModel(prefix='store1', inst=None)

        item1 = model.set(1)
        item2 = model.set(2)
        item2.hash['1'] = 1

        self.assertDictEqual(item1.data(), {'hash': {}, 'id': None, 'total': None})
        self.assertDictEqual(item2.data(), {'hash': {'1':1}, 'id': None, 'total': None})

    def test_clean_remove_all(self):
        model = StoreModel(prefix='1', inst=None)
        item = model.set(1)

        self.assertEqual(model.cursor.key, '1')
        self.assertEqual(item.cursor.key, '1:1')

        item.id.set(1)
        item.hash.set('2', '3')
        self.assertEqual(self.redis.hgetall('1:1'), {'id': '1'})
        self.assertEqual(self.redis.hgetall('1:1:hash'), {'2': '3'})
        self.assertEqual(self.redis.hgetall('1:_KEY'), {'1': '_KEY'})

        model.remove()

        self.assertEqual(self.redis.hgetall('1:1'), {})
        self.assertEqual(self.redis.hgetall('1:1:hash'), {})
        self.assertEqual(self.redis.hgetall('1'), {})


    def test_move(self):
        model = StoreModel(prefix='store', inst=None)
        item = model.set(1)
        item.id.set(2)
        self.assertEqual(len(model), 1)

        model.move(item.prefix, 2)
        self.assertEqual(len(model), 1)
        self.assertEqual(model.keys(), ['2'])


