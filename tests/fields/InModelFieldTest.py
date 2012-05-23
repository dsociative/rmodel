# coding: utf8

from model.rmodel import RModel
from model.rmodel_store import RModelStore
from redis.client import Redis
from unittest.case import TestCase

from model.fields.rfield2 import rfield2
from model.Cursor import Cursor

class rinmodel(rfield2):

    def inmodel_key(self, items):
        rt = []

        for i in items[:-1]:
            rt.append(i)

        rt.append('data')
        return Cursor(*rt).key

    def assign(self, inst):
        self.key = self.inmodel_key(inst.cursor.items)
        self.instance = inst
        self.redis = inst.redis

class StoreModel(RModel):

    names = rinmodel()

class TestModel(RModelStore):

    prefix = 'testmodel'
    assign = StoreModel



class TestInModelField(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()

        self.model = TestModel().set(1)
        self.field = self.model.names


    def test_(self):
        self.assertEqual(self.model.cursor.key, 'testmodel:1')
        self.assertEqual(self.field.key, 'testmodel:data')

        self.assertEqual(self.field(), None)
        self.field('we')
        self.assertEqual(self.field(), 'we')

