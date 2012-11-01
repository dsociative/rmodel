# -*- coding: utf-8 -*-


class RObject(object):

    root = False

    def init(self):
        pass

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.delete(self.key)
        self._session.add(self.cursor.items, self.data_default())

    def data_default(self):
        return self.default

    def process_data(self, values):
        value = values.pop(0)

        if not value:
            return self.data_default()
        else:
            return self.process_result(value)
