# coding: utf8

from model.fields.base_bound import BaseBound

class rzlist(BaseBound):
    '''
    Поле для работы с сортированными списками
    '''

    def __init__(self, _type=None, default=[], prefix=None, inst=None):
        super(rzlist, self).__init__(_type, default, prefix, inst)

    def data(self, redis=None, key=False):
        '''
        :returns: Список пар - *(ключ, счет)*
        
        >>> print [('key1', 10.0), ('key2', (11.0))]
        
        '''

        redis = redis or self.redis
        return redis.zrange(self.key, 0, -1, withscores=True)

    def add(self, name, score=0):
        '''
        :param name: имя поля
        :type name: str
        :param score: Начальный счет
        :type score: int, float
        
        Добавляет новую запись в список
        '''

        return self.redis.zadd(self.key, name, score)

    def remove(self, name):
        '''
        :param name: имя поля
        :type name: str
        
        Удаляет запись
        '''

        return self.redis.zrem(self.key, name)

    def incr(self, name, incr_by=1):
        '''
        :param name: Имя поля
        :type name: str
        :param incr_by: Значение на сколько будет увеличен счет поля
        :type incr_by: int, float
        
        Увеличивает счет поля
        '''

        return self.redis.zincrby(self.key, name, incr_by)

    def range(self, frm=0, to= -1, withscores=False, byscore=False):
        '''
        :param frm: Начальная позиция выборки
        :type frm: int
        :param to: Конечная позиция выборки
        :type to: int
        :param withscores: Опция позволяет выводить поля с их значениями
        :type withscores: bool
        '''

        if byscore:
            return self.redis.zrangebyscore(self.key, frm, to, withscores=withscores)
        else:
            return self.redis.zrange(self.key, frm, to, withscores=withscores)

    def rangebys(self, score):
        return  self.redis.zrangebyran()
