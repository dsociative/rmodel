# coding: utf8

from rmodel.common import dynamic_type
from rmodel.fields.base import RProperty
from rmodel.fields.unbound import Unbound


def onload(self, inst, field, data):
    return data


def onsave(self, inst, field, data):
    return data


class BaseBound(RProperty):

    root = False

    def __new__(cls, *args, **kwargs):
        if 'inst' in kwargs or cls.root:
            return super(RProperty, cls).__new__(cls, *args, **kwargs)
        else:
            return Unbound(cls, *args, **kwargs)

    def __init__(self, _type=dynamic_type, default=None, prefix=None, inst=None,
                 onload=onload, onsave=onsave):
        RProperty.__init__(self, _type=_type, default=default, prefix=prefix)
        self.assign(inst)
        self.init()

    def data_default(self):
        return self.default

    def fields(self):
        pass

    def process_data(self, values):
        value = values.pop(0)

        if not value:
            return self.data_default()
        else:
            return self.process_result(value)

    def onsave(self, value):
        return value

    def onload(self, value):
        return value

    def init(self):
        pass

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.delete(self.key)
