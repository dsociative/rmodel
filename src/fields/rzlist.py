# coding: utf8

from fields.base_bound import BaseBound


class rzlist(BaseBound):

    def data(self, redis=None, key=False):
        redis = redis or self.redis
        return redis.zrange(self.key, 0, -1, withscores=True)

    def data_default(self):
        return []

    def add(self, name, score=0):
        return self.redis.zadd(self.key, name, score)

    def remove(self, name):

        return self.redis.zrem(self.key, name)

    def incr(self, name, incr_by=1):
        return self.redis.zincrby(self.key, name, incr_by)

    def range(self, frm=0, to= -1, withscores=False, byscore=False):
        if byscore:
            return self.redis.zrangebyscore(self.key, frm, to,
                                            withscores=withscores)
        else:
            return self.redis.zrange(self.key, frm, to, withscores=withscores)

    def rangebys(self, score):
        return  self.redis.zrangebyran()
