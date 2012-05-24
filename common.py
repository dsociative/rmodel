# coding: utf8


class Run(object):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def action(self, obj, result):
        getattr(obj, self.name)(*self.args, **self.kwargs)
        return result

    def __call__(self, func):

        def w(obj, *a, **kw):
            result = func(obj, *a, **kw)
            return self.action(obj, result)

        return w


class ProxyRun(Run):

    def action(self, obj, result):
        getattr(result, self.name)(*self.args, **self.kwargs)
        return result
