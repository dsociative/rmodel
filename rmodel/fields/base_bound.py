# coding: utf8
from rmodel.fields.unbound import Unbound
from rmodel.sessions.base_session import BaseSession


class BaseBound(object):

    root = False

    def __new__(cls, *args, **kwargs):
        if 'inst' in kwargs or cls.root:
            return super(BaseBound, cls).__new__(cls, *args, **kwargs)
        else:
            return Unbound(cls, *args, **kwargs)

    # Model and Field usage

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
