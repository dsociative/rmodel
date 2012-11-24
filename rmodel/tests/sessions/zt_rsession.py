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

    def test_save_change_dict(self):
        rt = {}
        self.session._save_change(rt, 'nested', {'field': 'value'})
        self.eq(rt, {'nested': {'field': 'value'}})

        self.session._save_change(rt, 'nested', {'name': 'Vasya'})
        self.eq(rt, {'nested': {'name': 'Vasya'}})

    def test_save_change_list(self):
        rt = {}
        self.session._save_change(rt, 'scroll', ['one'])
        self.eq(rt, {'scroll': ['one']})

        self.session._save_change(rt, 'scroll', [2, 3])
        self.eq(rt, {'scroll': [2, 3]})

    def test_set_rfield_store(self):
        self.model.field.set('test')
        self.eq(self.session._store, [(('simple', 'field'), 'test')])

    def test_rfield_incr(self):
        self.model.field.set(10)
        self.session._store = []
        self.model.field += 5
        self.eq(self.session._store, [(('simple', 'field'), 15)])

    def test_append_rlist(self):
        self.model.scroll.append('one', 'two', 'orc')
        self.eq(self.session._store, [(('simple', 'scroll'),
                                       {0: 'one', 1: 'two', 2: 'orc'})])

    def test_rlist_set(self):
        self.model.scroll.set(['one', 'two'])
        self.eq(self.session._store, [(('simple', 'scroll'),
                                       ['one', 'two'])])

    def test_rhash_set(self):
        self.model.hash.set('goblin', 'attack')
        self.eq(self.session._store, [(('simple', 'hash', 'goblin'),
                                       'attack')])

    def test_rhash_clean(self):
        self.model.hash.clean()
        self.eq(self.session._store, [(('simple', 'hash'), {})])

    def test_rfield_in_stored_item(self):
        item = self.model.store.add()
        item.name.set('Orc?')
        self.eq(self.session._store, [(('simple', 'store', '1', 'name'),
                                        'Orc?')])

    def test_changes(self):
        self.session.add(('simple', 'field'), 'test')
        self.eq(self.session.changes(), {'simple': {'field': 'test'}})

    def test_changes_dict(self):
        self.session.add(('simple', 'hash'), {})
        self.eq(self.session.changes(), {'simple': {'hash': {}}})

    def test_two_field(self):
        self.session.add(('simple', 'power'), 100500)
        self.session.add(('simple', 'name'), 'Vasya')
        self.eq(self.session.changes(), {'simple': {'name': 'Vasya',
                                                    'power': 100500}})

    def test_two_nested(self):
        self.session.add(('', 'vasya', 'home', 'size'), 'big')
        self.session.add(('', 'goblin', 'cave', 'level'), 1)
        self.eq(self.session.changes(),
                {'': {'vasya': {'home': {'size': 'big'}},
                      'goblin': {'cave': {'level': 1}}}})

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
        self.eq(self.session.changes(), {'list': {3: 'value1', 4: 'value2',
                                                  5: 'value3'}})
