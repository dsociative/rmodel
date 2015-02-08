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


def test_set_get_data(model):
    assert model.id.get() == None
    assert model.name.get() == None

    model.id.set(1)
    assert model.id.get() == 1
    model.name.set('Тестовое имя')

    model = Model(redis=model.redis)

    assert model.id.get() == 1
    assert model.name.get() == 'Тестовое имя'
    assert model.data() == {'id': 1, 'name': 'Тестовое имя'}


def test_incr(model):
    assert model.id.get() is None
    model.id += 1
    assert model.id.get() == 1

    model.incr('id', 11)
    assert model.id.get() == 12

    model.id.set(10)
    assert model.id.get() == 10


def test_data(model):
    model.id.set(1)
    model.name.set('test_name')

    assert model.id.get() == 1
    assert model.name.get() == 'test_name'

    assert model.data() == {'id': 1, 'name': 'test_name'}


class StoreModel(RUnit):
    prefix = 'storemodel'
    store = rfield(int)


class NestedModel(Model):
    prefix = 'nested'
    name = rfield()
    nested = StoreModel()


@pytest.fixture
def nested_model(redis):
    return NestedModel(redis)


def test_nested_model(nested_model):
    assert len(nested_model.get_fields()) == 3
    nested_model.nested.store.set(1)
    assert nested_model.nested.store.get() == 1
    assert nested_model.data() == {
        'nested': {'store': 1}, 'id': None, 'name': None
    }


def test_redis_instance(nested_model, redis):
    assert nested_model.redis == redis
    assert nested_model.name.redis == redis
    assert nested_model.nested.redis == redis
    assert nested_model.nested.store.redis == redis


def test_defaults(model):
    model.defaults = {'id': 334, 'name': 'HELLO'}

    assert model.id.get() == 334
    assert model.name.get() == 'HELLO'


def test_session_remove(model, session):
    model._session = session
    model.remove()
    assert session.changes() == {model.prefix: None}