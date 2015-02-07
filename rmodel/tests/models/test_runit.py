# -*- coding: utf8 -*-
import pytest
from rmodel.fields.rfield import rfield
from rmodel.models.runit import RUnit


class Model(RUnit):
    prefix = 'testmodel'
    root = True

    id = rfield(int)
    name = rfield(prefix='name')


@pytest.fixture
def model(redis):
    return Model(redis)


def test_init_root(redis):
    model = Model(redis=redis)
    assert isinstance(model, RUnit)


def test_simple(model):
    assert model.id.get() == None
    assert model.name.get() == None

    model.id.set(1)
    assert model.id.get() == 1
    model.name.set('Тестовое имя')

    model = Model(redis=model.redis)

    assert model.id.get() == 1
    assert model.name.get() == 'Тестовое имя'
    assert model.data() == {'id': 1, 'name': 'Тестовое имя'}