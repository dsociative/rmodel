# coding: utf8

from fields.base_bound import BaseBound


class rhash(BaseBound):

    def __len__(self):
        return self.redis.hlen(self.key)

    def __contains__(self, key):
        return key in self.keys

    def data_default(self):
        return {}

    @property
    def keys(self):
        return self.redis.hkeys(self.key)

    def data(self, pipe=None, key=False):
        redis = pipe or self.redis
        value = redis.hgetall(self.key)

        if not pipe:
            return self.process(value)
        else:
            return value

    def onsave(self, field, value):
        return value

    def onload(self, field, value):
        return value

    def add(self, value):
        key = len(self)
        self.set(key, value)
        return key

    def set(self, field, value):
        return self.redis.hset(self.key, field, self.onsave(field, value))

    def get(self, field):
        value = self.redis.hget(self.key, field)
        return self.onload(field, self.process_result(value))

    def set_dict(self, value):
        return self.redis.hmset(self.key, value)

    def __setitem__(self, field, value):
        return self.set(field, value)

    def __getitem__(self, field):
        return self.get(field)

    def remove(self, field):
        return self.redis.hdel(self.key, field)

    def process_result(self, values):
        if type(values) is dict:
            for k, v in values.iteritems():
                values[k] = super(rhash, self).process_result(v)
            return values
        else:
            return super(rhash, self).process_result(values)

    def process(self, rt):
        for key, value in rt.iteritems():
            rt[key] = self.process_result(value)
        return rt

    def all(self):
        return self.data()
