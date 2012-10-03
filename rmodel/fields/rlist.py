# coding: utf8

from rmodel.fields.base_bound import BaseBound


class rlist(BaseBound):
    '''
    Поле для работы со списками
    '''

    def __contains__(self, value):
        return value in self.data()

    def data_default(self):
        return []

    def data(self, pipe=None, key=False):
        '''
        :returns: ['item1', 'item2']
        '''

        redis = pipe or self.redis
        value = redis.lrange(self.key, 0, -1)

        if not pipe:
            return [self.typer(i) for i in value]
        else:
            return value

    def append(self, *values):
        '''
        :param name: имя поля
        :type name: str
        :param score: Начальный счет
        :type score: int, float

        Добавляет новую запись в список
        '''
        self._session.add(self.cursor.items, list(values))
        return self.redis.rpush(self.key, *self.onsave(values))

    def process_result(self, rt):
        return [self.type(i) for i in rt]

    def __len__(self):
        return self.redis.llen(self.key)

    def range(self, frm=0, to=-1):
        '''
        :param frm: Начальная позиция выборки
        :type frm: int
        :param to: Конечная позиция выборки
        :type to: int
        :param withscores: Опция позволяет выводить поля с их значениями
        :type withscores: bool
        '''

        return self.redis.lrange(self.key, frm, to)

    def set(self, values):
        '''
        :param values: iterable values
        Clean and append new values
        '''
        self.clean()
        self.append(*values)

    def remove(self, value):
        '''
        :param value: value that must be removed
        '''
        return self.redis.lrem(self.key, value)

    def pop(self):
        return self.redis.lpop(self.key)

    def by_index(self, index):
        return self.redis.lindex(self.key, index)
