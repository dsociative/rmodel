# -*- coding: utf8 -*-
from rmodel.fields_iter import FieldsIter


class SessionCollector(FieldsIter):
    def __init__(self, redis, session, *fields):
        self.session = session
        self.redis = redis
        self._fields = list(self.get_fields(fields))

    def get_fields(self, fields):
        for field in fields:
            for f in self.process_field(field):
                yield f

    def process_field(self, field):
        if field.ismodel:
            return self.get_fields(field.get_fields())
        else:
            return field,

    collect = FieldsIter.data

    def process_data(self, values):
        for field in self._fields:
            self.session.add(field.cursor.items, field.process_data(values))