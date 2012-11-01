#coding: utf8
from rmodel.fields.rzlist import rzlist
from rmodel.tests.base_test import BaseTest


class RZListTest(BaseTest):

    def setUp(self):
        super(RZListTest, self).setUp()
        self.unbound = rzlist()
        self.model.init_fields([('names', self.unbound)])
        self.field = self.model.names

    def test_(self):
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

    def test_set(self):
        self.field.set('name', 1)
        self.eq(self.field.data(), [('name', 1)])
        self.field.set('name', 5)
        self.eq(self.field.data(), [('name', 5)])
        self.field.set('else')
        self.eq(self.field.data(), [('else', 0), ('name', 5)])

    def test_revrange(self):
        self.field.add('name1', 1)
        self.field.add('name2', 2)
        self.eq(self.field.revrange(), ['name2', 'name1'])

    def test_revrank(self):
        for i in xrange(5):
            self.field.add(str(i), i)
        self.eq(self.field.revrank('3'), 1)
