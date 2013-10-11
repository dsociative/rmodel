# coding: utf8
from rmodel.fields.base_field import BaseField


class rzlist(BaseField):

    def __contains__(self, value):
        return self.score(value) is not None
        
    def __len__(self):
        return self.redis.zcard(self.key)        

    def data(self):
        return self.collect_data(self.redis)

    def collect_data(self, pipe):
        return pipe.zrange(self.key, 0, -1, withscores=True)

    def data_default(self):
        return []

    def _db(self, pipe):
        return pipe or self.redis

    def add(self, name, score=0, pipe=None):
        self._field_changed(name, score)
        return self._db(pipe).zadd(self.key, name, score)

    def remove(self, name, pipe=None):
        self._field_changed(name, None)
        return self._db(pipe).zrem(self.key, name)

    def incr(self, name, incr_by=1):
        return self._field_changed(name, self.redis.zincrby(self.key, name, incr_by))

    def revrange(self, frm=0, to=-1, withscores=False):
        return self.redis.zrevrange(self.key, frm, to, withscores)

    def revrank(self, name):
        return self.redis.zrevrank(self.key, name)

    def range(self, frm=0, to=-1, withscores=False,
              byscore=False):

        if byscore:
            return self.redis.zrangebyscore(self.key, frm, to,
                                            withscores=withscores)
        else:
            return self.redis.zrange(self.key, frm, to, withscores=withscores)

    def score(self, value):
        return self.redis.zscore(self.key, value)
