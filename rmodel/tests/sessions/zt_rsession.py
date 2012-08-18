# coding: utf8

from rmodel.fields.rfield import rfield
from rmodel.fields.rhash import rhash
from rmodel.fields.rlist import rlist
from rmodel.models.rstore import RStore
from rmodel.models.runit import RUnit
from rmodel.sessions.rsession import RSession
from unittest.case import TestCase


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


class RSessionTest(TestCase):

    def setUp(self):
        RUnit.redis.flushall()
        self.session = RSession()
        self.model = SimpleModel(session=self.session)

    def test_save_change_dict(self):
        rt = {}
        self.session._save_change(rt, 'nested', {'field': 'value'})
        self.assertEqual(rt, {'nested': {'field': 'value'}})

        self.session._save_change(rt, 'nested', {'name': 'Vasya'})
        self.assertEqual(rt, {'nested': {'field': 'value',
                                         'name': 'Vasya'}})

    def test_save_change_list(self):
        rt = {}
        self.session._save_change(rt, 'scroll', ['one'])
        self.assertEqual(rt, {'scroll': ['one']})

        self.session._save_change(rt, 'scroll', [2, 3])
        self.assertEqual(rt, {'scroll': ['one', 2, 3]})

    def test_set_rfield_store(self):
        self.model.field.set('test')
        self.assertEqual(self.session._store, [(('simple',),
                                                {'field': 'test'})])

    def test_append_rlist(self):
        self.model.scroll.append('one', 'two', 'orc')
        self.assertEqual(self.session._store, [(('simple', 'scroll'),
                                    ['one', 'two', 'orc'])])

    def test_rhash_set(self):
        self.model.hash.set('goblin', 'attack')
        self.assertEqual(self.session._store, [(('simple', 'hash'),
                                                {'goblin': 'attack'})])

    def test_rhash_clean(self):
        self.model.hash.clean()
        self.assertEqual(self.session._store, [(('simple', 'hash'), {})])

    def test_rfield_in_stored_item(self):
        item = self.model.store.add()
        item.name.set('Orc?')
        self.assertEqual(self.session._store, [(('simple', 'store', '1'),
                                                {'name': 'Orc?'})])

    def test_changes(self):
        self.session.add(('simple',), 'test', 'field')
        self.assertEqual(self.session.changes(), {'simple': {'field': 'test'}})

    def test_changes_dict(self):
        self.session.add(('simple', 'hash'), {})
        self.assertEqual(self.session.changes(), {'simple': {'hash': {}}})

    def test_two_field(self):
        self.session.add(('simple',), 100500, 'power')
        self.session.add(('simple',), 'Vasya', 'name')
        self.assertEqual(self.session.changes(),
                         {'simple': {'name': 'Vasya', 'power': 100500}})

    def test_two_nested(self):
        self.session.add(('', 'vasya', 'home'), 'big', 'size')
        self.session.add(('', 'goblin', 'cave'), 1, 'level')
        self.assertEqual(self.session.changes(),
                         {'': {'vasya': {'home': {'size': 'big'}},
                               'goblin': {'cave': {'level': 1}}}})

    def test_nested_list_changes(self):
        self.session.add(('root', 'nested', 'scroll'), ['one', 'two'])
        self.assertEqual(self.session.changes(),
                         {'root': {'nested': {'scroll': ['one', 'two']}}})
        self.session.add(('root', 'nested', 'scroll'), ['tree', ])
        self.assertEqual(self.session.changes(),
                         {'root': {'nested': {'scroll': ['one', 'two',
                                                         'tree']}}})
