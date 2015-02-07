# coding: utf8
import pytest
from rmodel.cursor import Cursor


@pytest.mark.parametrize('cursor,key', [
    (Cursor('user', 100), 'user:100'),
    (Cursor('user', 100, 'location'), 'user:100:location'),
    (Cursor('user', 100).new('location'), 'user:100:location'),
    (Cursor('user', 100).new('location').new('1'), 'user:100:location:1'),
    (Cursor('user', 100).new('location').new(1), 'user:100:location:1'),
    (Cursor('user', 100).new('location', 2), 'user:100:location:2'),
    (Cursor('user', 100).new('location', '2'), 'user:100:location:2'),
])
def test_key(cursor, key):
    assert cursor.key == key
