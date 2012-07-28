# coding: utf8

from cursor import Cursor
from unittest.case import TestCase

class CursorTest(TestCase):

    def setUp(self):
        self.cursor = Cursor('user', 100)

    def test_key(self):
        self.assertEqual(self.cursor.key, 'user:100')

    def test_none(self):
        new = self.cursor.new('location')
        self.assertEqual(new.key, 'user:100:location')
        new = new.new('1')
        self.assertEqual(new.key, 'user:100:location:1')


    def test_new(self):
        new = self.cursor.new('location', 2)
        self.assertEqual(new.key, 'user:100:location:2')

    def test_dict(self):
        new = self.cursor.new('location', 2)
        self.assertEqual(new.dict, {'user': {100: {'location': {2: {}}}}})

    def test_dict_nested(self):
        new = self.cursor.new('locations', 2).new('buildings', 3)
        self.assertEqual(new.changes({'id':2}),
                         {'user':{100:{'locations':{2:{'buildings':{3:{'id':2}}}}}}})

    def test_dict_odd(self):
        new = self.cursor.new('locations', 2).new('buildings',)
        self.assertEqual(new.changes({'id':2}),
                         {'user':{100:{'locations':{2:{'buildings':{'id':2}}}}}})
