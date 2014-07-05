# coding: utf8
from rmodel.models.base_model import BaseModel


class RStore(BaseModel):

    KEYS_PREFIX = '_KEY'
    INCR_KEY = '_INCR'

    def __init__(self, *args, **kwargs):
        super(RStore, self).__init__(*args, **kwargs)
        self._key_cursor = self.cursor.new(self.KEYS_PREFIX)

    def _contains(self, redis, prefix):
        return redis.sismember(self._key_cursor.key, prefix)

    def __contains__(self, prefix):
        return self._contains(self.redis, prefix)

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
        self._add_key(self.redis, key)

    def _add_key(self, redis, key):
        redis.sadd(self._key_cursor.key, key)

    def incr_key(self):
        return self.redis.hincrby(self.cursor.key, self.INCR_KEY)

    def add(self, args=(), session=None):
        return self.set(self.incr_key(), args, session=session)

    def get(self, prefix, session=None):
        if prefix in self:
            return self.init_model(prefix, session)

    def create_new_model(self, args, prefix, session):
        model = self.init_model(prefix, session=session)
        model.new(*args)
        return model

    def set(self, prefix, args=(), session=None):
        self.add_key(prefix)
        return self.create_new_model(args, prefix, session)

    def pipe(self, func, values):
        p = self.redis.pipeline()
        for value in values:
            func(p, value)
        return p.execute()

    def mset_gen(self, prefixes, args=(), session=None):
        self.pipe(self._add_key, prefixes)

        for prefix in prefixes:
            yield self.create_new_model(args, prefix, session)

    def mset(self, prefixes, args=(), session=None):
        return list(self.mset_gen(prefixes, args, session))

    def mget_gen(self, prefixes, session=None):
        for prefix, exist in zip(
                prefixes, self.pipe(self._contains, prefixes)
        ):
            if exist:
                yield self.init_model(prefix, session)

    def mget(self, prefixes, session=None):
        return list(self.mget_gen(prefixes, session))

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
