# -*- coding: utf-8 -*-


class RObject:

    root = False

    def init(self):
        pass

    def clean(self, pipe=None, inst=None):
        raise NotImplemented

    def process_data(self, values):
        raise NotImplemented
