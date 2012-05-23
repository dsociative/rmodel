# coding: utf8

from fields.base import RProperty
from fields.base_bound import BaseBound


class rfield(BaseBound):

    def assign(self, inst):
        self.key = inst.cursor.key
        self.instance = inst
        self.redis = inst.redis

    def __init__(self, _type=str, default=None, prefix=None, inst=None):
        RProperty.__init__(self, _type=_type, default=default, prefix=prefix)
        self.assign(inst)

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.hdel(self.key, self.prefix)

    def set(self, value):
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
