# coding: utf8

from fields.rfield import rfield
from rmodel import RModel
from rmodel_store import RModelStore


class DeepModel(RModel):

    value = rfield()

class TItem(RModel):

    id = rfield(int, 0)
    value = rfield()
    deep = DeepModel

class TDB(RModelStore):

    assign = TItem


