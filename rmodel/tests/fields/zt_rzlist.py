#coding: utf8
from rmodel.fields.rzlist import rzlist
from rmodel.sessions.rsession import RSession
from rmodel.tests.base_test import BaseTest


class rzlistBaseTest(BaseTest):

    def setUp(self):
        super(rzlistBaseTest, self).setUp()
        self.unbound = rzlist()
        self.model.init_fields([('names', self.unbound)])
        self.field = self.model.names


class rzlistTest(rzlistBaseTest):

    def test_add(self):
        self.eq(self.model.names.data_default(), [])
        self.eq(self.model.data(), {'names': []})

        self.field.add('uid1', 555)
        self.eq(self.model.data(), {'names': [('uid1', 555.0)]})

        self.field.add('uid2', 553)
        self.eq(self.model.names.data(), [('uid2', 553.0),
            ('uid1', 555.0)])

    def test_del(self):
        self.field.add('uid1', 555)
        self.eq(self.field.range(), ['uid1'])
        self.field.remove('uid1')
        self.eq(self.field.range(), [])

    def test_incr(self):
        self.eq(self.field.data(), [])
        self.field.add('incr_key')
        self.eq(self.field.data(), [('incr_key', 0)])
        self.field.incr('incr_key', 10)
        self.eq(self.field.data(), [('incr_key', 10)])
        self.field.incr('incr_key')
        self.eq(self.field.data(), [('incr_key', 11)])

    def test_range(self):
        fields = ['fields%s' % i for i in xrange(3)]

        for no, field in enumerate(fields):
            self.field.add(field, no)

        self.eq(self.field.range(), fields)
        self.eq(self.field.range(withscores=True), self.field.data())
        self.eq(self.field.range(1, 2, withscores=True),
            [('fields1', 1.0), ('fields2', 2.0)])

    def test_revrange(self):
        self.field.add('name1', 1)
        self.field.add('name2', 2)
        self.eq(self.field.revrange(), ['name2', 'name1'])

    def test_score(self):
        self.eq(self.field.score('test'), None)
        self.field.add('test', 30)
        self.eq(self.field.score('test'), 30)
        self.field.add('something', 50)
        self.eq(self.field.score('something'), 50)

    def test_revrank(self):
        for i in xrange(5):
            self.field.add(str(i), i)
        self.eq(self.field.revrank('3'), 1)

    def test_exists(self):
        self.false('test' in self.field)
        self.field.add('test')
        self.true('test' in self.field)


class rzlistSessionTest(rzlistBaseTest):

    def setUp(self):
        super(rzlistSessionTest, self).setUp()
        self.field._session = RSession()

    def test_save(self):
        self.field.add('name', 50)
        self.field.add('other', 30)
        self.eq(self.field._session._store,
                {'model': {'names': {'other': 30, 'name': 50}}})

    def test_incr(self):
        self.field.add('other', 30)
        self.field.incr('other', 30)
        self.eq(self.field._session._store,
                        {'model': {'names': {'other': 60}}})

    def test_remove(self):
        self.field.remove('name')
        self.field.remove('other')
        self.eq(self.field._session._store,
                {'model': {'names': {'other': None, 'name': None}}})
