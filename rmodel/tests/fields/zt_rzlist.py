#coding: utf8
from fields.rfield import rfield
from fields.rzlist import rzlist
from redis.client import Redis
from rmodel.models.runit import RUnit
from unittest.case import TestCase


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





