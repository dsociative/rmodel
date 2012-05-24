#coding: utf8

from common import Run
from cursor import Cursor
from fields import RBase
from fields.base_bound import BaseBound
from redis.client import Redis


class RModel(BaseBound):

    defaults = False

    redis = Redis()
    prefix = ''

    def __new__(self, *args, **kwargs):
        self.class_fields = dict(self.fields_gen())
        return object.__new__(self, *args, **kwargs)

    @classmethod
    def fields_gen(cls):
        for name in dir(cls):
            field = getattr(cls, name)
            if issubclass(field.__class__, RBase) and name != 'assign':
                yield name, field

    @Run('init')
    def __init__(self, cursor=Cursor(), prefix=None, inst=None):
        if prefix is not None:
            self.prefix = str(prefix)
        self.cursor = cursor.new(self.prefix)
        self._fields = tuple(self.init_fields())
        self.instance = inst

    def init_fields(self):
        for name, field in self.class_fields.items():
            yield field.bound(self, name)

    @property
    def fields(self):
        return self._fields

    @classmethod
    def bound(cls, inst, prefix):
        field = cls(inst.cursor, prefix, inst=inst)
        setattr(inst, field.prefix, field)
        return field

    def __setitem__(self, field, value):
        return self.redis.hset(self.cursor.key, field, value)

    def __getitem__(self, field):
        return self.redis.hget(self.cursor.key, field)

    def __delitem__(self, field):
        return self.redis.hdel(self.cursor.key, field)

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
                result[field.prefix] = self.process_data(field.fields,
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
        for field in self.fields:
            field.clean(pipe, self)

    def data(self, pipe=None, key=None):
        child = True

        if not pipe:
            child = False
            pipe = self.redis.pipeline()

        for field in self.fields:
            field.data(pipe, key=self.cursor.key)

        if not child:
            values = map(self.typer, pipe.execute())
            return self.process_data(self.fields, values)

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

