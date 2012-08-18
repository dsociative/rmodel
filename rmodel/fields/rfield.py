# coding: utf8

from rmodel.fields.base_bound import BaseBound


class rfield(BaseBound):

    def assign(self, inst):
        self.cursor = inst.cursor
        self.instance = inst
        self.redis = inst.redis

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.hdel(self.cursor.key, self.prefix)
        self._session.add(self.cursor.items, None, self.prefix)

    def data(self, redis, key):
        return redis.hget(key, self.prefix)

    def set(self, value):
        self._session.add(self.cursor.items, value, field=self.prefix)
        return self.redis.hset(self.cursor.key, self.prefix, self.onsave(value))

    def get(self):
        return self.process_result(self.data(self.redis, self.cursor.key))

    def onincr(self, value):
        return value

    def incr(self, value):
        value = self.redis.hincrby(self.cursor.key, self.prefix,
                                   self.onincr(value))
        self._session.add(self.cursor.items, value, self.prefix)
        return self

    def __isub__(self, value):
        return self.incr(-value)

    def __iadd__(self, value):
        return self.incr(value)
