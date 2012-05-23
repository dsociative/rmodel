# coding: utf8

from model.rmodel import RModel
from model.rmodel_store import RModelStore
from model.fields.rfield import rfield


class DeepModel(RModel):

    value = rfield()

class TItem(RModel):

    id = rfield(int, 0)
    value = rfield()
    deep = DeepModel

class TDB(RModelStore):

    assign = TItem


