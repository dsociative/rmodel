# coding: utf8
from rmodel.fields.rfield import rfield
from rmodel.fields.rhash import rhash
from rmodel.models.rstore import RStore
from rmodel.models.runit import RUnit
from rmodel.sessions.rsession import RSession
from rmodel.tests.base_test import BaseTest


class ItemModel(RUnit):

    id = rfield(int)
    total = rfield(int)
    hash = rhash(int, 0)


class StoreModel(RStore):

    assign = ItemModel

    prefix = 'store'
    name = rfield(str, 'default_name')


class IndexModel(RUnit):

    prefix = 'model'
    root = True

    lenght = rfield()
    store = StoreModel()


class NewItem(RUnit):

    field = rfield()

    def new(self, value):
        self.field.set(value)


class NewTestModel(RStore):

    root = True
    assign = NewItem


class BaseRStoreTest(BaseTest):

    def setUp(self):
        super(BaseRStoreTest, self).setUp()
        self.session = RSession()
        self.model = IndexModel(session=self.session, redis=self.redis)


class RStoreTest(BaseRStoreTest):

    def test_init(self):
        self.assertIsInstance(self.model, IndexModel)
        self.eq(self.model.redis, self.redis)

    def test_session(self):
        self.eq(self.session, self.model.store._session)

    def test_session_inherit(self):
        self.eq(self.session, self.model.store.add()._session)

    def test_session_override_get(self):
        session = RSession()
        self.model.store.set(1)
        self.eq(session, self.model.store.get(1, session)._session)

    def test_session_override_add_set(self):
        session = RSession()
        self.eq(session, self.model.store.add(session=session)._session)
        self.eq(session, self.model.store.set(2, session=session)._session)

    def test_with_model(self):
        model = StoreModel(inst=None, redis=self.redis)
        self.eq(model.data(), {'name': 'default_name'})

    def test_custom_new_with_args(self):
        model = NewTestModel(redis=self.redis)
        item = model.add(args=('test_values',))
        self.eq(item.field.get(), 'test_values')
        item = model.set('test', args=('somthing_else',))
        self.eq(item.field.get(), 'somthing_else')


class RUnitItemTest(BaseRStoreTest):

    def setUp(self):
        super(RUnitItemTest, self).setUp()
        self.item = self.model.store.add()

    def test_redis(self):
        self.eq(self.item.redis, self.redis)

    def test_instance(self):
        self.true(isinstance(self.item, ItemModel), True)

    def test_data(self):
        self.item.id.set(1)
        self.item.total.set(1)
        self.eq(self.item.data(), {'id': 1, 'hash': {}, 'total': 1})

    def test_two_item(self):
        self.item.total.set(2)
        self.item.id.set(1)

        item2 = self.model.store.set(2)
        item2.id.set(8)
        item2.total.set(4)
        self.eq(self.item.id.get(), 1)
        self.eq(self.item.total.get(), 2)

        self.eq(self.item.data(), {'total': 2, 'hash': {}, 'id': 1})
        self.eq(item2.data(), {'total': 4, 'hash': {}, 'id': 8})
        self.eq(self.model.store.data(),
                {'1': {'hash': {}, 'id': 1, 'total': 2},
                 '2': {'hash': {}, 'id': 8, 'total': 4},
                 'name': 'default_name'})

    def test_keys(self):
        self.eq(self.model.store.keys(), ['1'])
        self.eq(1 in self.model.store, True)
        self.eq(len(self.model.store), 1)

        self.eq(self.model.store.new_key(), long(2))
        item = self.model.store.add()
        self.eq(self.model.store.new_key(), long(4))
        self.eq(len(self.model.store), 2)

    def test_clean_remove_all(self):
        self.eq(self.model.cursor.key, 'model')
        self.eq(self.item.cursor.key, 'model:store:1')

        self.item.id.set(1)
        self.item.hash.set('2', '3')

        self.eq(self.redis.hgetall(self.item.cursor.key), {'id': '1'})
        self.eq(self.redis.hgetall(self.item.hash.cursor.key), {'2': '3'})
        self.eq(self.redis.hgetall(self.model.store._key_cursor.key),
                {'1': '_KEY', '_INCR': '1'})

        self.model.remove()

        self.eq(self.redis.hgetall('1:1'), {})
        self.eq(self.redis.hgetall('1:1:hash'), {})
        self.eq(self.redis.hgetall('1'), {})

    def test_remove(self):
        self.item.total = 2
        self.item.id = 1

        self.assertTrue(self.model.store.get(1))
        self.model.store.remove_item(1)
        self.assertFalse(self.model.store.get(1))

    def test_move(self):
        self.item.id.set(2)
        self.eq(len(self.model.store), 1)

        self.model.store.move(self.item.prefix, 2)
        self.eq(len(self.model.store), 1)
        self.eq(self.model.store.keys(), ['2'])

    def test_two_models(self):
        item2 = self.model.store.set(2)
        item2.hash['1'] = 1

        self.eq(self.item.data(), {'hash': {}, 'id': None, 'total': None})
        self.eq(item2.data(), {'hash': {'1': 1}, 'id': None, 'total': None})
