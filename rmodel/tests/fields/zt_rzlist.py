#coding: utf8
from rmodel.fields.rfield import rfield
from rmodel.fields.rzlist import rzlist
from redis.client import Redis
from rmodel.models.runit import RUnit
from unittest2.case import TestCase


class TestModel(RUnit):
    prefix = 'testmodel'
    root = True

    id = rfield(int)
    names = rzlist()


class Test(TestCase):
    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.model = TestModel()
        self.field = self.model.names

    def test_(self):
        self.assertEqual(self.model.names.data_default(), [])
        self.assertEqual(self.model.data(), {'id': None, 'names': []})

        self.field.add('uid1', 555)
        self.assertEqual(self.model.data(), {'id': None,
                                             'names': [('uid1', 555.0)]})

        self.field.add('uid2', 553)
        self.assertEqual(self.model.names.data(), [('uid2', 553.0),
            ('uid1', 555.0)])

    def test_del(self):
        self.field.add('uid1', 555)
        self.assertEqual(self.field.range(), ['uid1'])
        self.field.remove('uid1')
        self.assertEqual(self.field.range(), [])

    def test_incr(self):
        self.assertEqual(self.field.data(), [])
        self.field.add('incr_key')
        self.assertEqual(self.field.data(), [('incr_key', 0)])
        self.field.incr('incr_key', 10)
        self.assertEqual(self.field.data(), [('incr_key', 10)])
        self.field.incr('incr_key')
        self.assertEqual(self.field.data(), [('incr_key', 11)])

    def test_range(self):
        fields = ['fields%s' % i for i in xrange(3)]

        for no, field in enumerate(fields):
            self.field.add(field, no)

        self.assertEqual(self.field.range(), fields)
        self.assertEqual(self.field.range(withscores=True), self.field.data())
        self.assertEqual(self.field.range(1, 2, withscores=True),
            [('fields1', 1.0), ('fields2', 2.0)])

    def test_set(self):
        self.field.set('name', 1)
        self.assertEqual(self.field.data(), [('name', 1)])
        self.field.set('name', 5)
        self.assertEqual(self.field.data(), [('name', 5)])
        self.field.set('else')
        self.assertEqual(self.field.data(), [('else', 0), ('name', 5)])

    def test_revrange(self):
        self.field.add('name1', 1)
        self.field.add('name2', 2)
        self.assertEqual(self.field.revrange(), ['name2', 'name1'])
