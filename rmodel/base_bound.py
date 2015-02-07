# coding: utf8
from rmodel.fields.unbound import Unbound
from rmodel.robject import RObject


class BaseBound(RObject):

    ismodel = False

    def __new__(cls, *args, **kwargs):
        if cls.isinit(kwargs):
            return super(BaseBound, cls).__new__(cls)
        else:
            return Unbound(cls, *args, **kwargs)

    @classmethod
    def isinit(cls, kwargs):
        return 'inst' in kwargs or cls.root
