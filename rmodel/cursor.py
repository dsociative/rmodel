# coding: utf8


class Cursor(object):

    separator = ':'

    def __init__(self, *items):
        self.items = items
        self.key = Cursor.separator.join(self.items_to_str(items))

    def items_to_str(self, args):
        return map(str, args)

    def new(self, *items):
        return Cursor(*self.subkey(*items))

    def subkey(self, *items):
        return self.items + items

