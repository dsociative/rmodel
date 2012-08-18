# coding: utf8


class Unbound(object):

    __unbound__ = 1

    def __init__(self, cls, *args, **kwargs):
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def init(self, inst=None, prefix=''):
        self.kwargs['inst'] = inst
        self.kwargs['prefix'] = prefix
        self.kwargs['session'] = inst._session

        return self.cls(*self.args, **self.kwargs)

    def bound(self, inst, prefix):
        field = self.init(inst, prefix)
        setattr(inst, field.prefix or prefix, field)
        return field

    def __repr__(self):
        rt = [self.cls.__name__, ]

        default = self.kwargs.get('default')
        if default is not None:
            rt.append('default: %s' % default)

        return ', '.join(rt)
