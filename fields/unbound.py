#coding: utf8

from fields import RBase


class Unbound(RBase):

    __unbound__ = 1

    def __init__(self, cls, *args, **kwargs):
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def init(self, inst=None, prefix=''):
        self.kwargs['inst'] = inst
        self.kwargs['prefix'] = prefix

        return self.cls(*self.args, **self.kwargs)

    def bound(self, inst, prefix):
        field = self.init(inst, prefix)
        setattr(inst, field.prefix or prefix, field)
        return field
