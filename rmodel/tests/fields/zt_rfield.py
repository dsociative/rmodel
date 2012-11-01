#coding: utf8
from rmodel.fields.rfield import rfield
from rmodel.models.runit import RUnit
from rmodel.tests.base_test import BaseTest


class RfieldTest(BaseTest):

    def setUp(self):
        super(RfieldTest, self).setUp()
        self.unbound = rfield(int, 0)
        self.unbound.bound(self.model, 'field')

    def test_init(self):
        self.eq(self.model.field.get(), 0)

    def test_incr(self):
        self.model.field -= 10
        self.eq(self.model.field.get(), -10)
