# coding: utf8
from rmodel.fields.rset import rset
from rmodel.tests.base_test import BaseTest


class RSetTest(BaseTest):

    def setUp(self):
        super(RSetTest, self).setUp()
        self.unbound = rset()
        self.model.init_fields([('names', self.unbound)])
        self.field = self.model.names

    def test_default(self):
        self.eq(self.field.data(), [])

    def test_append(self):
        self.field.append('name')
        self.eq(self.field.data(), ['name'])
        self.field.append('thatever')
        self.eq(self.field.data(), ['thatever', 'name'])

    def test_append_dublication(self):
        self.field.append('name')
        self.field.append('name')
        self.eq(self.field.data(), ['name'])

    def test_pop_none(self):
        self.eq(self.field.pop(), None)

    def test_pop(self):
        self.field.append('name')
        self.eq(self.field.pop(), 'name')
        self.eq(self.field.data(), [])

    def test_remove_null(self):
        self.eq(self.field.remove('name'), 0)

    def test_remove(self):
        self.field.append('name')
        self.eq(self.field.remove('name'), 1)
        self.eq(self.field.data(), [])

    def test_len(self):
        self.eq(len(self.field), 0)
        self.field.append('name')
        self.field.append('name')
        self.eq(len(self.field), 1)
        self.field.append('name2')
        self.eq(len(self.field), 2)

    def test_contents(self):
        self.not_in('name', self.field)
        self.field.append('name')
        self.isin('name', self.field)
