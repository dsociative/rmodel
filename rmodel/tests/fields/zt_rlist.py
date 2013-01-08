#coding: utf8

from rmodel.fields.rlist import rlist
from rmodel.sessions.rsession import RSession
from rmodel.tests.base_test import BaseTest


class rlistBaseTest(BaseTest):

    def setUp(self):
        super(rlistBaseTest, self).setUp()

        self.unbound = rlist()
        self.model.init_fields([('names', self.unbound)])
        self.field = self.model.names


class rlistTest(rlistBaseTest):

    def test_range(self):
        self.eq(self.model.names.range(), [])
        self.eq(self.model.data(), {'names': []})

        self.eq(len(self.field), 0)
        self.field.append('myname')
        self.eq(self.field.range(), ['myname'])
        self.field.append('sd')
        self.eq(self.field.range(), ['myname', 'sd'])
        self.eq(len(self.field), 2)
        self.field.append('one', 'two')
        self.eq(self.field.range(), ['myname', 'sd', 'one', 'two'])

    def test_pop(self):
        self.eq(self.field.range(), [])
        self.field.append('value1', 1)
        self.eq(self.field.range(), ['value1', 1])
        self.eq(self.field.pop(), 'value1')
        self.eq(self.field.pop(), 1)
        self.eq(self.field.pop(), None)

    def test_set(self):
        self.field.set(['123', '42'])
        self.eq(self.field.range(), [123, 42])

    def test_typing(self):
        self.field.type = int
        self.field.set(['123', '42'])

        self.eq(self.model.data(), {'names': [123, 42]})
        self.eq(self.model.names.range(), [123, 42])

    def test_remove(self):
        self.model.names.append('hello', 'test')
        self.model.names.remove('hello')
        self.eq(self.model.names.range(), ['test'])
        self.model.names.remove('not_in_redis_key')
        self.eq(self.model.names.range(), ['test'])

    def test_remove_similar(self):
        for _ in xrange(2):
            self.field.append('value')

        self.field.remove('value', 1)
        self.eq(self.field.range(), ['value'])

    def test_by_index(self):
        self.eq(self.field.by_index('hello'), None)
        self.field.append('hello')
        self.eq(self.field.by_index(0), 'hello')
        self.field.append('next')
        self.eq(self.field.by_index(1), 'next')
        self.field.append(2)
        self.eq(self.field.by_index(2), 2)

    def test_trim(self):
        self.field.append(*xrange(10))
        self.field.trim(1, 12)
        self.eq(self.field.range(), list(xrange(1, 10)))
        self.field.trim(0, 0)
        self.eq(self.field.range(), [1])

    def test_contains_false(self):
        self.eq('hello' in self.model.names, False)

    def test_contains_true(self):
        self.model.names.append('hello')
        self.eq('hello' in self.model.names, True)


class rlistSessionTest(rlistBaseTest):

    def setUp(self):
        super(rlistSessionTest, self).setUp()
        self.session = self.field._session = RSession()

    def test_remove(self):
        self.field.append('test')
        self.field.remove('test')
        self.eq(self.session._store, {'model': {'names': {0: None}}})
