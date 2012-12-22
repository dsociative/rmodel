# coding: utf8
from rmodel.fields.base_field import BaseField


class rlist(BaseField):
    """
    Поле для работы со списками
    """

    def __contains__(self, value):
        return value in self.range()

    def data_default(self):
        return []

    def collect_data(self, pipe):
        return pipe.lrange(self.key, 0, -1)

    def __push(self, values):
        return self.redis.rpush(self.key, *self.onsave(values))

    def append(self, *values):
        """
        :param name: имя поля
        :type name: str
        :param score: Начальный счет
        :type score: int, float

        Добавляет новую запись в список
        """
        return self._session.append(self.cursor.items, values,
                                    self.__push(values))

    def process_result(self, rt):
        return [self.typer(i) for i in rt]

    def __len__(self):
        return self.redis.llen(self.key)

    def range(self, frm=0, to=-1):
        """
        :param int frm: Начальная позиция выборки
        :param int to: Конечная позиция выборки
        """

        return self.process_result(self.redis.lrange(self.key, frm, to))

    def set(self, values):
        """
        :param values: iterable values
        Clean and append new values
        """
        self.redis.delete(self.key)
        self.__push(values)
        self._session.add(self.cursor.items, values)

    def remove(self, value, count=0):
        """
        http://redis.io/commands/lrem
        """
        return self.redis.lrem(self.key, value, count)

    def pop(self):
        return self.typer(self.redis.lpop(self.key))

    def trim(self, frm, to):
        return self.redis.ltrim(self.key, frm, to)

    def by_index(self, index):
        return self.typer(self.redis.lindex(self.key, index))
