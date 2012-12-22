# coding: utf8
from rmodel.fields.rset import rset
from rmodel.tests.base_test import BaseTest
from rmodel.tests.fields.zt_field_session import FieldSessionTest


class RSetBaseTest(BaseTest):
    def setUp(self):
        super(RSetBaseTest, self).setUp()
        self.unbound = rset()
        self.model.init_fields([('names', self.unbound)])
        self.field = self.model.names


class RSetTest(RSetBaseTest):

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


class RSetSessionTest(FieldSessionTest, RSetBaseTest):

    def test_add(self):
        self.field.append('name', 'something')
        self.field.append('else')
        self.eq(self.session.changes(),
                {'model': {'names': {'name': 1, 'something': 1, 'else': 1}}})

    def test_remove(self):
        self.field.append('name')
        self.field.remove('name')
        self.eq(self.session.changes(),
                {'model': {'names': {'name': None}}})

    def test_pop(self):
        self.field.append('name')
        self.field.pop()
        self.eq(self.session.changes(),
                {'model': {'names': {'name': None}}})
