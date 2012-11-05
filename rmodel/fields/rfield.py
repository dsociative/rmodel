# coding: utf8
from rmodel.fields.base_field import BaseField


class rfield(BaseField):

    def assign(self, inst):
        self.cursor = inst.cursor
        self.instance = inst

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.hdel(self.cursor.key, self.prefix)
        self._session.add(self.cursor.items, None, self.prefix)

    def collect_data(self, pipe):
        return pipe.hget(self.cursor.key, self.prefix)

    def set(self, value):
        self._session.add(self.cursor.items, value, field=self.prefix)
        return self.redis.hset(self.cursor.key, self.prefix,
                               self.onsave(value))

    def get(self):
        return self.process_result(self.collect_data(self.redis))

    def onincr(self, value):
        return value

    def incr(self, value):
        value = self.redis.hincrby(self.cursor.key, self.prefix,
                                   self.onincr(value))
        self._session.add(self.cursor.items, value, self.prefix)
        return value

    def __isub__(self, value):
        self.incr(-value)
        return self

    def __iadd__(self, value):
        self.incr(value)
        return self
