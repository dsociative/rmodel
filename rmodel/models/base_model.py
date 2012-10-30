# -*- coding: utf-8 -*-
from rmodel.fields.base_bound import BaseBound


no_changes = {}


class BaseModel(BaseBound):

    def fields(self):
        pass
