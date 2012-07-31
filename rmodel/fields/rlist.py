# coding: utf8

from fields.base_bound import BaseBound


class rlist(BaseBound):
    '''
    Поле для работы с сортированными списками
    '''

    def __init__(self, _type=None, default=[], prefix=None, inst=None):
        super(rlist, self).__init__(_type, default, prefix, inst)

    def data(self, redis=None, key=False):
        '''
        :returns: Список        
        >>> print [('key1', 10.0), ('key2', (11.0))]
        
        '''

        redis = redis or self.redis
        return redis.lrange(self.key, 0, -1)

    def append(self, *values):
        '''
        :param name: имя поля
        :type name: str
        :param score: Начальный счет
        :type score: int, float
        
        Добавляет новую запись в список
        '''

        return self.redis.rpush(self.key, *values)

    def __len__(self):
        return self.redis.llen(self.key)

    def range(self, frm=0, to= -1, withscores=False):
        '''
        :param frm: Начальная позиция выборки
        :type frm: int
        :param to: Конечная позиция выборки
        :type to: int
        :param withscores: Опция позволяет выводить поля с их значениями
        :type withscores: bool
        '''

        return self.redis.lrange(self.key, frm, to)
