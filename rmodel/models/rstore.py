# coding: utf8
from rmodel.models.base_model import BaseModel


class RStore(BaseModel):

    KEYS_PREFIX = '_KEY'
    INCR_KEY = '_INCR'

    def __init__(self, *args, **kwargs):
        super(RStore, self).__init__(*args, **kwargs)
        self._key_cursor = self.cursor.new(self.KEYS_PREFIX)

    def __contains__(self, prefix):
        return self.redis.sismember(self._key_cursor.key, prefix)

    def __len__(self):
        return self.redis.scard(self._key_cursor.key)

    def keys(self):
        return self.redis.smembers(self._key_cursor.key)

    def items(self):
        return self.redis.hgetall(self.cursor.key).items()

    def models(self, session=None):
        for key in self.keys():
            yield self.init_model(key, session)

    def fields(self):
        for model in self.models():
            yield model
        for field in self._fields:
            yield field

    def move(self, start, end):
        self.delete_key(start)
        self.set(end)
        self.redis.rename(self.cursor.new(start).key, self.cursor.new(end).key)

    def init_model(self, prefix, session=None):
        if session is None:
            session = self._session

        return self.assign(prefix=prefix, inst=self, session=session,
                           redis=self.redis)

    def add_key(self, key):
        self.redis.sadd(self._key_cursor.key, key)

    def incr_key(self):
        return self.redis.hincrby(self.cursor.key, self.INCR_KEY)

    def add(self, args=(), session=None):
        return self.set(self.incr_key(), args, session=session)

    def get(self, prefix, session=None):
        if prefix in self:
            return self.init_model(prefix, session)

    def set(self, prefix, args=(), session=None):
        self.add_key(prefix)
        model = self.init_model(prefix, session=session)
        model.new(*args)
        return model

    def remove_item(self, prefix):
        item = self.get(prefix)
        if item:
            self.remove_model(item)

    def remove_model(self, item):
        item.remove()
        self.delete_key(item.prefix)

    def delete_key(self, prefix):
        return self.redis.srem(self._key_cursor.key, prefix)

    def clean(self, pipe):
        super(RStore, self).clean(pipe)

        pipe.delete(self.cursor.key)
        pipe.delete(self._key_cursor.key)
