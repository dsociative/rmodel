# -*- coding: utf-8 -*-
from rmodel.models.base_model import BaseModel


class FieldsIter(object):

    def __init__(self, model, iter_class=None):
        self.iter_class = iter_class or self.__class__

        self.model = model
        self.prefix = model.prefix

        self._fields = list(self.get_fields(model))

    def get_fields(self, model):
        for field in self.model.fields():
            yield self.process_field(field)

    def process_field(self, field):
        if issubclass(field.__class__, BaseModel):
            return self.iter_class(field)
        else:
            return field

    def data(self):
        pipe = self.model.redis.pipeline()
        self.collect_data(pipe)
        return self.process_data(pipe.execute())

    def collect_data(self, pipe):
        for field in self:
            field.collect_data(pipe)

    def process_data(self, values):
        result = {}
        for field in self:
            result[field.prefix] = field.process_data(values)
        return result

    def __iter__(self):
        return iter(self._fields)
