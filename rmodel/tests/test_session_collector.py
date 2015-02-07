# -*- coding: utf8 -*-
import pytest
from redis import Redis

from rmodel.fields.rfield import rfield
from rmodel.models.runit import RUnit
from rmodel.session_collector import SessionCollector


class TestModel(RUnit):
    prefix = 'test_model'
    root = True
    field1 = rfield()
    field2 = rfield()


def test_fields(model, session):
    collector = SessionCollector(model.redis, session, model)
    assert sorted(collector._fields) == sorted([model.field1, model.field2])


def test_collect(model, session):
    model.field1.set('1a')
    model.field2.set(3)
    SessionCollector(model.redis, session, model).collect()
    assert session.changes() == {'test_model': {'field1': '1a', 'field2': 3}}


def test_collect_one_field(model, session):
    model.field2.set('onefield')
    SessionCollector(model.redis, session, model.field2).collect()
    assert session.changes() == {'test_model': {'field2': 'onefield'}}
