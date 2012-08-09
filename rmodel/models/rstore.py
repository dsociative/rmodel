# coding: utf8

from rmodel.common import Run, ProxyRun
from rmodel.models.runit import RUnit


class RStore(RUnit):

    KEY = '_KEY'
    INCR_KEY = '_INCR'

    @Run('init')
    def __init__(self, prefix=None, inst=None):
        RUnit.__init__(self, prefix=prefix, inst=inst)
        self._key_cursor = self.cursor.new(self.KEY)

    def __contains__(self, prefix):
        return self.redis.hexists(self._key_cursor.key, prefix)

    def __len__(self):
        if self.redis.hexists(self._key_cursor.key, self.INCR_KEY):
            shift = 1
        else:
            shift = 0
        return self.redis.hlen(self._key_cursor.key) - shift

    def keys(self):

        def ismodel_key(key):
            return key != self.INCR_KEY

        return filter(ismodel_key, self.redis.hkeys(self._key_cursor.key))

    def items(self):
        return self.redis.hgetall(self.cursor.key).items()

    def models(self):
        for key in self.keys():
            yield self.get(key)

    def fields(self):
        for model in self.models():
            yield model
        for field in self._fields:
            yield field

    def move(self, start, end):
        self.delete_key(start)
        self.set(end)
        self.redis.rename(self.cursor.new(start).key, self.cursor.new(end).key)

    def init_model(self, prefix):
        return self.assign(prefix=prefix, inst=self)

    def add(self, *args, **kwargs):
        return self.set(self.new_key(), *args, **kwargs)

    def get(self, prefix):
        if prefix in self:
            return self.init_model(prefix)

    def set(self, prefix, *args, **kwargs):
        self.redis.hset(self._key_cursor.key, prefix, self.KEY)
        model = self.init_model(prefix)
        model.new(*args, **kwargs)
        return model

    def new_key(self):
        return self.redis.hincrby(self._key_cursor.key, self.INCR_KEY)

    def delete_key(self, prefix):
        return self.redis.hdel(self._key_cursor.key, prefix)

    def remove_item(self, prefix):
        item = self.get(prefix)
        if item:
            item.remove()
            self.delete_key(prefix)

    def clean(self, pipe, inst):
        RUnit.clean(self, pipe, inst)

        pipe.delete(self.cursor.key)
        pipe.delete(self._key_cursor.key)
