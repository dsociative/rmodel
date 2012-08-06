# coding: utf8

from rmodel.fields.base_bound import BaseBound


class rset(BaseBound):
    '''
    Redis sets field http://redis.io/commands#set
    '''

    def data_default(self):
        return []

    def data(self, pipe=None, key=False):
        '''
        :returns: ['item1', 'item2']
        '''

        redis = pipe or self.redis
        value = redis.smembers(self.key)

        if not pipe:
            return [self.typer(i) for i in value]
        else:
            return value

    def append(self, *values):
        return self.redis.sadd(self.key, *self.onsave(values))

    def pop(self):
        '''
        pop random value from redis
        http://redis.io/commands/spop
        '''
        return self.redis.spop(self.key)
