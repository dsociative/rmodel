# -*- coding: utf-8 -*-
from rmodel.common import dynamic_type
from rmodel.fields.unbound import Unbound
from rmodel.sessions.base_session import BaseSession

from rmodel.fields.base_bound import BaseBound
no_session = BaseSession()


class BaseField(BaseBound):

    def __init__(self, _type=dynamic_type, default=None, prefix=None,
                 inst=None, session=None):

        self._default = default
        self.prefix = prefix
        self.type = _type

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
        self.redis = inst.redis

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
