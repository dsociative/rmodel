# coding: utf8

from fields.base import RProperty
from fields.unbound import Unbound


def onload(self, inst, field, data):
    return data


def onsave(self, inst, field, data):
    return data


class BaseBound(RProperty):
    '''
    Базовый класс, за счет которого поля модели при компиляции отдают :class:`Unbound`,
    который хранит поля и их настройки.
    '''
    def __new__(cls, *args, **kwargs):
        if 'inst' in kwargs:
            return super(RProperty, cls).__new__(cls, *args, **kwargs)
        else:
            return Unbound(cls, *args, **kwargs)

    def __init__(self, _type=str, default=None, prefix=None, inst=None,
                 onload=onload, onsave=onsave):
        RProperty.__init__(self, _type=_type, default=default, prefix=prefix)
        self.assign(inst)
        self.init()

    def onsave(self, value):
        return value

    def onload(self, value):
        return value

    def init(self):
        pass

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.delete(self.key)
