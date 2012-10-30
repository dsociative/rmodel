# coding: utf8
from rmodel.fields.base_field import BaseField


class rzlist(BaseField):

    def data(self, redis=None, key=False):
        redis = redis or self.redis
        return redis.zrange(self.key, 0, -1, withscores=True)

    def data_default(self):
        return []

    def _db(self, pipe):
        return pipe or self.redis

    def add(self, name, score=0, pipe=None):
        return self._db(pipe).zadd(self.key, name, score)

    def set(self, name, score=0):
        pipe = self.redis.pipeline()
        self.remove(name, pipe)
        self.add(name, score, pipe)
        return pipe.execute()

    def remove(self, name, pipe=None):
        return self._db(pipe).zrem(self.key, name)

    def incr(self, name, incr_by=1):
        return self.redis.zincrby(self.key, name, incr_by)

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

    def rangebys(self, score):
        return  self.redis.zrangebyran()
