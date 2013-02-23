# coding: utf8
from rmodel.fields.base_field import BaseField


class rhash(BaseField):

    def __len__(self):
        return self.redis.hlen(self.key)

    def __contains__(self, field):
        return self._exists(self.redis, field)

    def _exists(self, redis, field):
        return redis.hexists(self.key, field)

    def data_default(self):
        return {}

    @property
    def keys(self):
        return self.redis.hkeys(self.key)

    def values(self):
        return self.process_list(self.redis.hvals(self.key))

    def data(self):
        return self.process_result(self.collect_data(self.redis))

    def collect_data(self, pipe):
        return pipe.hgetall(self.key)

    def onsave(self, field, value):
        return value

    def onload(self, field, value):
        return value

    def add(self, value):
        key = len(self)
        self.set(key, value)
        return key

    def set(self, field, value):
        self._field_changed(field, value)
        return self.redis.hset(self.key, field, self.onsave(field, value))

    def get(self, field):
        value = self.redis.hget(self.key, field)
        return self.onload(field, self.typer(value))

    def mget(self, *fields):
        return self.process_list(self.redis.hmget(self.key, *fields))

    def incr(self, field, value=1):
        value = self.typer(self.redis.hincrby(self.key, field, value))
        return self._field_changed(field, value)

    def set_dict(self, value):
        pipe = self.redis.pipeline()
        self._change(value)

        self.clean(pipe)
        if value:
            self._set_dict(pipe, value)

        return pipe.execute()

    def _set_dict(self, redis, value):
        return redis.hmset(self.key, value)

    def __setitem__(self, field, value):
        return self.set(field, value)

    def __getitem__(self, field):
        return self.get(field)

    def remove(self, field):
        return self.redis.hdel(self.key, field)

    def process_result(self, rt):
        return self.process_dict(rt)

    def process_dict(self, rt):
        for key, value in rt.iteritems():
            rt[key] = self.typer(value)
        return rt

