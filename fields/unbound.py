#coding: utf8

class Unbound(object):

    redis_field = True

    def __init__(self, cls, *args, **kwargs):
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def bound(self, inst, prefix):

        self.kwargs['inst'] = inst
        self.kwargs['prefix'] = prefix

        field = self.cls(*self.args, **self.kwargs)
        setattr(inst, field.prefix or prefix, field)
        return field
