# coding: utf8
from rmodel.cursor import Cursor
from rmodel.tests.base_test import BaseTest


class CursorTest(BaseTest):

    def setUp(self):
        self.cursor = Cursor('user', 100)

    def test_key(self):
        self.eq(self.cursor.key, 'user:100')

    def test_none(self):
        new = self.cursor.new('location')
        self.eq(new.key, 'user:100:location')
        new = new.new('1')
        self.eq(new.key, 'user:100:location:1')

    def test_new(self):
        new = self.cursor.new('location', 2)
        self.eq(new.key, 'user:100:location:2')
