# -*- coding: utf-8 -*-
from rmodel.base_bound import BaseBound
from rmodel.common import dynamic_type


class BaseField(BaseBound):

    def __init__(self, _type=dynamic_type, default=None, prefix=None,
                 inst=None, session=None, redis=None):

        self._default = default
        self.prefix = prefix
        self.type = _type
        self.redis = redis

        self._session = session
        self.assign(inst)
        self.init()

    def onsave(self, value):
        return value

    def onload(self, value):
        return value

    def assign(self, inst):
        self.cursor = inst.cursor.new(self.prefix)
        self.key = self.cursor.key
        self.instance = inst

    def typer(self, value):
        if value is not None:
            return self.type(value)
        else:
            return self.default

    def process_result(self, rt):
        return self.typer(rt)

    @property
    def default(self):
        if not self._default is None:
            return self._default
        elif self.instance.defaults:
            return self.instance.defaults.get(self.prefix)

    def process_data(self, values):
        value = values.pop(0)

        if not value:
            return self.data_default()
        else:
            return self.process_result(value)

    def clean(self, pipe=None, inst=None):
        pipe = pipe or self.redis
        pipe.delete(self.key)
        self._session.add(self.cursor.items, self.data_default())

    def data_default(self):
        return self.default
