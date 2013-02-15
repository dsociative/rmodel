# -*- coding: utf-8 -*-
from rmodel.base_bound import BaseBound
from rmodel.common import Run
from rmodel.cursor import Cursor
from rmodel.fields_iter import FieldsIter
from rmodel.sessions.base_session import BaseSession


no_changes = {}
no_session = BaseSession()


class BaseModel(BaseBound):

    defaults = False
    prefix = ''
    ismodel = True

    def fields(self):
        raise NotImplementedError()

    def new(self):
        pass

    @Run('init')
    def __init__(self, redis, prefix=None, inst=None, session=no_session):
        self.redis = redis
        self._session = session
        if prefix is not None:
            self.prefix = str(prefix)

        if inst is not None:
            self.cursor = inst.cursor.new(self.prefix)
        else:
            self.cursor = Cursor(self.prefix)

        self._fields = []
        self.instance = inst
        self.init_fields(self.fields_gen())

    @classmethod
    def fields_gen(cls):
        for name in dir(cls):
            field = getattr(cls, name)
            if hasattr(field, '__unbound__'):
                yield name, field

    def init_fields(self, fields):
        for name, field in fields:
            self._fields.append(field.bound(self, name))

    def data(self):
        return FieldsIter(self).data()

    def collect_data(self, pipe):
        for field in self.fields():
            field.collect_data(pipe)

    def clean(self, pipe):
        for field in self.fields():
            field.clean(pipe)

    def typer(self, value):
        return value

    def remove(self):
        pipe = self.redis.pipeline()
        self.clean(pipe)
        self._session.add(self.cursor.items, None)
        pipe.execute()
