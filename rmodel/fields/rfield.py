# coding: utf8

from rmodel.fields.base_bound import BaseBound


class rfield(BaseBound):

    def assign(self, inst):
        self.key = inst.cursor.key
        self.instance = inst
        self.redis = inst.redis

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.hdel(self.key, self.prefix)
        self._changes = None

    def data(self, redis, key):
        return redis.hget(key, self.prefix)

    def set(self, value):
        self._changes = value
        return self.redis.hset(self.key, self.prefix, self.onsave(value))

    def get(self):
        return self.process_result(self.data(self.redis, self.key))

    def onincr(self, value):
        return value

    def __isub__(self, value):
        self.redis.hincrby(self.key, self.prefix, self.onincr(-value))
        return self

    def __iadd__(self, value):
        self.redis.hincrby(self.key, self.prefix, self.onincr(value))
        return self
