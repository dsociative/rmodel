# coding: utf8

from common import ProxyRun
from unittest.case import TestCase


class ProxyObj(object):

    def __init__(self, *arg, **kwarg):
        self.arg = arg
        self.kwarg = kwarg

    def new(self):
        self.id = 3


class TestProxyRun(object):

    @ProxyRun('new')
    def obj(self, *arg, **kwarg):
        return ProxyObj(*arg, **kwarg)


class CommonTest(TestCase):

    def test_(self):
        t = TestProxyRun()
        obj = t.obj(1, 2, new=True)

        self.assertEqual(obj.arg, (1, 2))
        self.assertEqual(obj.kwarg, {'new': True})
        self.assertEqual(obj.id, 3)

