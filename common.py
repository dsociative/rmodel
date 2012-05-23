# coding: utf8


class ProxyRun(object):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):

        def w(obj, *a, **kw):
            result = func(obj, *a, **kw)
            getattr(result, self.name)(*self.args, **self.kwargs)
            return result

        return w

