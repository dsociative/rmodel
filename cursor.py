# coding: utf8

def deep_copy(orig):
    rt = orig.copy()
    for key, value in rt.items():
        if type(value) is dict:
            rt[key] = deep_copy(value)
    return rt

class Cursor(object):

    separator = ':'

    def pairs(self, seq):
        if len(seq) % 2:
            seq.append(None)

        return seq[::2], seq[1::2]

    def make_data(self, args):
        result = {}
        keys = filter(lambda x: x != None, list(args))

        path = []
        for collection, value in zip(*self.pairs(keys)):
            result, path = self.dump(result, collection, value, path)
        return result

    def current_nested(self, rt, args):
        nested = rt
        for i in args:
            nested = nested[i]
        return nested

    def dump(self, rt, collection, value, args=[]):
        current = self.current_nested(rt, args)
        current[collection] = {value:{}} if value else {}

        args += collection, value
        return rt, args

    def __init__(self, *args):
        self.items = args
        self.key = Cursor.separator.join(self.str(args))
        self.dict = self.make_data(args)

    def to_dict(self, args):
        keys = args[::2]
        values = args[1::2]
        return dict(zip(keys, values))

    def changes_in(self, data):
        return self.to_dict(list(self.items) + [data])


    def changes(self, kwargs):
        rt = deep_copy(self.dict)
        nested = self.current_nested(rt, self.items)
        nested.update(kwargs)
        return rt

    def subkey(self, *args):
        return self.items + args

    def new(self, *args):
        return Cursor(*self.subkey(*args))

    def str(self, args):
        return map(str, args)
