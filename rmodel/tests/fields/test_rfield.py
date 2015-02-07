#coding: utf8
import pytest
from rmodel.fields.rfield import rfield
from rmodel.models.runit import RUnit


@pytest.fixture
def model(redis):

    class Model(RUnit):
        prefix = 'model'
        root = True

    return Model(redis=redis)


@pytest.fixture
def field(model):
    f = rfield(int, 0)
    return f.bound(model, 'field')


def test_init(field):
    assert isinstance(field, rfield)
    assert field.get() == 0


def test_cursor(field):
    assert field.cursor.items == ('model', 'field')


def test_incr(field):
    field -= 10
    assert field.get() == -10