#coding: utf8

from common import Run
from cursor import Cursor
from fields.base_bound import BaseBound
from redis.client import Redis


class RModel(BaseBound):

    defaults = False

    redis = Redis()
    prefix = ''

    @classmethod
    def fields_gen(cls):
        for name in dir(cls):
            field = getattr(cls, name)
            if hasattr(field, '__unbound__'):
                yield name, field

    @Run('init')
    def __init__(self, prefix=None, inst=None):
        self.class_fields = dict(self.fields_gen())
        if prefix is not None:
            self.prefix = str(prefix)

        if inst is not None:
            self.cursor = inst.cursor.new(self.prefix)
        else:
            self.cursor = Cursor(self.prefix)

        self._fields = tuple(self.init_fields())
        self.instance = inst

    def init_fields(self):
        for name, field in self.class_fields.items():
            yield field.bound(self, name)

    def fields(self):
        return self._fields

    @classmethod
    def bound(cls, inst, prefix):
        field = cls(inst.cursor, prefix, inst=inst)
        setattr(inst, field.prefix, field)
        return field

    def typer(self, value):
        if type(value) is str and value.isdigit():
            value = int(value)
        elif type(value) is dict:
            for k, v in value.items():
                value[k] = self.typer(v)
        return value

    def process_data(self, fields, values):
        result = {}
        for field in fields:
            if issubclass(field.__class__, RModel):
                result[field.prefix] = self.process_data(field.fields(),
                                                            values)
            else:
                value = values.pop(0)
                if value is None:
                    value = field.default
                result[field.prefix] = value

        return result

    def remove(self):
        pipe = self.redis.pipeline()
        self.clean(pipe, self)
        pipe.execute()

    def clean(self, pipe, inst):
        for field in self.fields():
            field.clean(pipe, self)

    def data(self, pipe=None, key=None):
        child = True

        if not pipe:
            child = False
            pipe = self.redis.pipeline()

        for field in self.fields():
            field.data(pipe, key=self.cursor.key)

        if not child:
            values = map(self.typer, pipe.execute())
            return self.process_data(self.fields(), values)

    def incr(self, sect, key, val=1):
        section = getattr(self, sect)
        if not section.get(key):
            section[key] = val
        else:
            section[key] += val

    def decr(self, sect, key, val=1):
        section = getattr(self, sect)
        section[key] -= val
        if not section.get(key):
            section.remove(key)

    def new(self):
        pass

    def init(self):
        pass

