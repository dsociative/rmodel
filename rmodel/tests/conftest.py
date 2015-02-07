# -*- coding: utf8 -*-
from redis import Redis
import pytest
from rmodel.sessions.rsession import RSession


@pytest.fixture
def redis():
    r = Redis(db=9, decode_responses=True)
    r.flushdb()
    return r


@pytest.fixture
def session():
    return RSession()