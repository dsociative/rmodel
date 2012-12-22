# coding: utf8
from rmodel.fields.base_field import BaseField


class rset(BaseField):
    """
    Redis sets field http://redis.io/commands#set
    """

    def __len__(self):
        """
        Get the number of members in a set
        http://redis.io/commands/scard
        """
        return self.redis.scard(self.key)

    def __contains__(self, name):
        """
        Determine if a given value is a member of a set
        http://redis.io/commands/sismember
        """
        return self.redis.sismember(self.key, name)

    def data_default(self):
        return []

    def data(self):
        """
        :returns: ['item1', 'item2']
        """
        return [self.typer(i) for i in self.collect_data(self.redis)]

    def collect_data(self, pipe):
        return pipe.smembers(self.key)

    def _values_changed(self, values, status):
        for value in values:
            self._field_changed(value, status)

    def append(self, *values):
        self.redis.sadd(self.key, *self.onsave(values))
        return self._values_changed(values, 1)

    def pop(self):
        """
        pop random value from redis
        http://redis.io/commands/spop
        """
        value = self.redis.spop(self.key)
        self._field_changed(value, None)
        return value

    def remove(self, key):
        """
        :param key: to remove from set
        http://redis.io/commands/srem
        """
        self._field_changed(key, None)
        return self.redis.srem(self.key, key)
