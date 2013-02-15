# -*- coding: utf-8 -*-
from rmodel.tests.base_test import BaseTest
from rmodel.models.runit import RUnit
from rmodel.fields.rfield import rfield
from rmodel.fields_iter import FieldsIter


class SimpleModel(RUnit):

    name = rfield()
    uid = rfield(int)


class NestedModel(RUnit):

    some = rfield()
    nested = SimpleModel()


class FieldsIterTest(BaseTest):

    def setUp(self):
        super(FieldsIterTest, self).setUp()
        self.model = SimpleModel(self.redis, inst=None)
        self.model.name.set('nick')
        self.model.uid.set('1')
        self.gen = FieldsIter(self.model)

    def test_process_fields(self):
        self.eq(self.gen.process_field(self.model.name), self.model.name)

    def test_get_fields(self):
        self.eq(list(self.gen.get_fields()),
                [self.model.name, self.model.uid])

    def test_process(self):
        self.eq(self.gen.process_data(['nick', '23']),
                {'name': 'nick', 'uid': 23})

    def test_simple_fields(self):
        self.eq(self.gen._fields, [self.model.name, self.model.uid])
        self.eq(list(self.gen), self.gen._fields)
        self.eq(list(self.gen), self.gen._fields)

    def test_simple_data(self):
        self.eq(self.gen.data(), {'name': 'nick', 'uid': 1})


class FieldsNestedTest(BaseTest):

    def setUp(self):
        super(FieldsNestedTest, self).setUp()
        self.model = NestedModel(self.redis, inst=None)
        self.model.some.set('nested')
        self.model.nested.name.set('nick')
        self.model.nested.uid.set('1')
        self.gen = FieldsIter(self.model)

    def test_process_field(self):
        processed = self.gen.process_field(self.model.nested)
        self.isinstance(processed, self.gen.iter_class)

    def test_fields(self):
        self.eq(len(self.gen._fields), 2)
        nested_gen = self.gen._fields[0]
        self.isinstance(nested_gen, self.gen.iter_class)
        self.eq(self.gen._fields[1], self.model.some)

    def test_data(self):
        self.eq(self.gen.data(), {'nested': {'name': 'nick', 'uid': 1},
                                  'some': 'nested'})

