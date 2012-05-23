#coding: utf8
from cursor import Cursor
from redis.client import Redis

def ismodel(field):
    return hasattr(field, 'model')

def isfield(field):
    return hasattr(field, 'redis_field')

class MetaModel(type):

    def __init__(cls, name, bases, attrs):
        cls._fields = {}
        for name in dir(cls):
            field = getattr(cls, name)
            if (ismodel(field) or isfield(field)) and name != 'assign':
                cls._fields[name] = field
        type.__init__(cls, name, bases, attrs)


class RModel(object):

    __metaclass__ = MetaModel
    defaults = False

    model = True
    redis_field = True

    redis = Redis()
    prefix = ''

    def inherit(self, inst):
        self.instance = inst

    def __init__(self, cursor=Cursor(), prefix=None, inst=None):
        if prefix is not None:
            self.prefix = str(prefix)
        self.cursor = cursor.new(self.prefix)

        rt = {}
        for name, field in self._fields.items():
            field = field.bound(self, name)
            rt[name] = field
        self._fields = rt

        self.inherit(inst)

    def move(self, cursor):
        if self.redis.exists(self.cursor.key):
            self.redis.rename(self.cursor.key, cursor.key)
        self.cursor = cursor

        for field in self.fields:
            if ismodel(field):
                field.move(self.cursor.new(field.prefix))

    @property
    def fields(self):
        return self._fields.values()

    @property
    def _setting(self):
        return self.fields

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
            if not ismodel(field):
                value = values.pop(0)
                if value is None:
                    value = field.default
                result[field.prefix] = value
            else:
                result[field.prefix] = self.process_data(field.fields,
                                                            values)
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
            return self.process_data(self._setting, values)

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

