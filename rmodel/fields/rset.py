# coding: utf8
from rmodel.fields.base_field import BaseField


class rset(BaseField):
    '''
    Redis sets field http://redis.io/commands#set
    '''

    def __len__(self):
        '''
        Get the number of members in a set
        http://redis.io/commands/scard
        '''
        return self.redis.scard(self.key)

    def __contains__(self, name):
        '''
        Determine if a given value is a member of a set
        http://redis.io/commands/sismember
        '''
        return self.redis.sismember(self.key, name)

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

    def remove(self, key):
        '''
        :param key: to remove from set
        http://redis.io/commands/srem
        '''
        return self.redis.srem(self.key, key)
