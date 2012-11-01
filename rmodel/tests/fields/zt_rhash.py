#coding: utf8
from rmodel.fields.rhash import rhash
from rmodel.fields.unbound import Unbound
from rmodel.tests.base_test import BaseTest
from rmodel.tests.base_test import TModel


class RHashTest(BaseTest):

    def setUp(self):
        super(RHashTest, self).setUp()
        self.unbound = rhash(int, 0)
        self.model.init_fields((('hash', self.unbound),))

    def test_unbound(self):
        self.assertIsInstance(rhash('test', int, 0), Unbound)
        self.assertIsInstance(self.unbound, Unbound)

    def test_bound(self):
        bound_field = self.unbound.bound(self.model, 'test')
        self.assertIsInstance(bound_field, rhash)

        bound_field['q'] = 1
        self.assertEqual(bound_field.data(), {'q': 1})
        self.assertEqual(bound_field.prefix, 'test')

    def test_two_model(self):
        model2 = TModel(prefix='2', redis=self.redis)
        model2.init_fields([('hash', self.unbound)])

        model2.hash['1'] = 1

        self.eq(self.model.data(), {'hash': {}})
        self.eq(model2.data(), {'hash': {'1': 1}})
