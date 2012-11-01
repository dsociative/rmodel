# -*- coding: utf-8 -*-
from redis.client import Redis
from ztest import ZTest
from rmodel.models.runit import RUnit


class TModel(RUnit):

    prefix = 'model'
    root = True


class BaseTest(ZTest):

    def setUp(self):
        self.redis = Redis()
        self.redis.flushdb()
        self.model = TModel(redis=self.redis)
