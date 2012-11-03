# -*- coding: utf-8 -*-
from rmodel.base_bound import BaseBound
from rmodel.common import Run
from rmodel.cursor import Cursor
from rmodel.sessions.base_session import BaseSession


no_changes = {}
no_session = BaseSession()


class BaseModel(BaseBound):

    defaults = False
    prefix = ''

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

    def data(self, pipe=None):
        child = True

        if not pipe:
            child = False
            pipe = self.redis.pipeline()

        for field in self.fields():
            field.data(pipe)

        if not child:
            values = map(self.typer, pipe.execute())
            return self.process_data(values)

    def process_data(self, values):
        result = {}
        for field in self.fields():
            result[field.prefix] = field.process_data(values)
        return result

    def clean(self, pipe, inst):
        for field in self.fields():
            field.clean(pipe, self)

    def typer(self, value):
        return value
