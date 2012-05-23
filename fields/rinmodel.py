# coding: utf8

from model.fields.rfield import rfield
from model.cursor import Cursor

class rinmodel(rfield):

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
        self.prefix_hash = '%s@%s' % (inst.prefix, self.prefix)

    def data(self, redis, key):
        return redis.hget(self.key, self.prefix_hash)

    def set(self, value):
        return self.redis.hset(self.key, self.prefix_hash, self.onsave(value))

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.hdel(self.key, self.prefix_hash)

    def __isub__(self, value):
        self.redis.hincrby(self.key, self.prefix_hash, self.onincr(-value))
        return self

    def __iadd__(self, value):
        self.redis.hincrby(self.key, self.prefix_hash, self.onincr(value))
        return self
