#coding: utf8
from model import RModel, rfield
from model.fields.rlist import rlist
from redis.client import Redis
from unittest.case import TestCase

class TestModel(RModel):

    prefix = 'testmodel'

    id = rfield(int)
    names = rlist()

class Test(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.model = TestModel()
        self.field = self.model.names

    def test_(self):
        self.assertEqual(self.model.names.default, [])
        self.assertEqual(self.model.data(), {'id': None, 'names': []})

        self.assertEqual(len(self.field), 0)
        self.field.append('myname')
        self.assertEqual(self.field.data(), ['myname'])
        self.field.append('sd')
        self.assertEqual(self.field.data(), ['myname', 'sd'])
        self.assertEqual(len(self.field), 2)






