# coding: utf8
from rmodel.fields.rfield import rfield
from rmodel.fields.rhash import rhash
from rmodel.fields.rlist import rlist
from rmodel.models.rstore import RStore
from rmodel.models.runit import RUnit
from rmodel.sessions.rsession import RSession
from rmodel.tests.base_test import BaseTest


class ItemModel(RUnit):

    name = rfield()


class StoreModel(RStore):

    assign = ItemModel


class SimpleModel(RUnit):

    root = True
    prefix = 'simple'

    field = rfield()
    hash = rhash()
    scroll = rlist()

    store = StoreModel()


class RSessionTest(BaseTest):

    def setUp(self):
        super(RSessionTest, self).setUp()
        self.session = RSession()
        self.model = SimpleModel(session=self.session, redis=self.redis)

    def test_flush(self):
        self.session.add(('1', '2'), 'value')
        self.session.flush()
        self.eq(self.session.changes(), {})

    def test_path_destination(self):
        self.eq(self.session.path_destination(('name', 'something', 'dest')),
                (('name', 'something'), 'dest'))

    def test_set_by_path(self):
        self.session.set_by_path(('root', 'field', 'name'), 'Vasya')
        self.eq(self.session._store, {'root': {'field': {'name': 'Vasya'}}})

    def test_pave_path(self):
        self.eq(self.session.pave_path(('root', 'field', 'name')),
                ({}, 'name'))

    def test_set_rfield_store(self):
        self.model.field.set('test')
        self.eq(self.session._store, {'simple': {'field': 'test'}})

    def test_rfield_incr(self):
        self.model.field.set(10)
        self.model.field += 5
        self.eq(self.session._store, {'simple': {'field': 15}})

    def test_append_rlist(self):
        self.model.scroll.append('one', 'two', 'orc')
        self.eq(self.session._store,
                {'simple': {'scroll': {0: 'one', 1: 'two', 2: 'orc'}}})

    def test_rlist_set(self):
        self.model.scroll.set(['one', 'two'])
        self.eq(self.session._store, {'simple': {'scroll': ['one', 'two']}})

    def test_rhash_set(self):
        self.model.hash.set('goblin', 'attack')
        self.eq(self.session._store, {'simple': {'hash': {'goblin': 'attack'}}})

    def test_rhash_delete(self):
        self.model.hash.delete()
        self.eq(self.session._store, {'simple': {'hash': {}}})

    def test_rfield_delete(self):
        self.model.field.delete()
        self.eq(self.session._store, {'simple': {'field': None}})

    def test_rfield_in_stored_item(self):
        item = self.model.store.add()
        item.name.set('Orc?')
        self.eq(self.session._store,
                {'simple': {'store': {'1': {'name': 'Orc?'}}}})

    def test_nested_list_changes(self):
        self.session.add(('root', 'nested', 'scroll'), ['one', 'two'])
        self.eq(self.session.changes(),
                {'root': {'nested': {'scroll': ['one', 'two']}}})
        self.session.add(('root', 'nested', 'scroll'), ['tree', ])
        self.eq(self.session.changes(),
                {'root': {'nested': {'scroll': ['tree']}}})

    def test_none_changes(self):
        self.session.add(('model', 'nested', '1'), None)
        self.eq(self.session.changes(), {'model': {'nested': {'1': None}}})

    def test_append(self):
        self.session.append(('list',), ['value'], 1)
        self.eq(self.session.changes(), {'list': {0: 'value'}})

    def test_append_many(self):
        self.session.append(('list',), ['value1', 'value2', 'value3'], 6)
        self.session.append(('list',), ['q'], 9)
        self.eq(self.session.changes(), {'list': {3: 'value1', 4: 'value2',
                                                  5: 'value3', 8: 'q'}})
