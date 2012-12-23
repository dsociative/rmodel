# coding: utf8
from rmodel.models.base_model import BaseModel


class RStore(BaseModel):

    KEY = '_KEY'
    INCR_KEY = '_INCR'

    def __init__(self, *args, **kwargs):
        super(RStore, self).__init__(*args, **kwargs)
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

    def add(self, args=(), session=None):
        return self.set(self.new_key(), args, session=session)

    def get(self, prefix, session=None):
        if prefix in self:
            return self.init_model(prefix, session)

    def set(self, prefix, args=(), session=None):
        self.redis.hset(self._key_cursor.key, prefix, self.KEY)
        model = self.init_model(prefix, session=session)
        model.new(*args)
        return model

    def new_key(self):
        return self.redis.hincrby(self._key_cursor.key, self.INCR_KEY)

    def remove_item(self, prefix):
        item = self.get(prefix)
        if item:
            self.remove_model(item)

    def remove_model(self, item):
        item.remove()
        self.delete_key(item.prefix)

    def delete_key(self, prefix):
        return self.redis.hdel(self._key_cursor.key, prefix)

    def clean(self, pipe, inst):
        super(RStore, self).clean(pipe, inst)

        pipe.delete(self.cursor.key)
        pipe.delete(self._key_cursor.key)
