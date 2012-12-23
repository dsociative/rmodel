#coding: utf8
from rmodel.models.base_model import BaseModel


class RUnit(BaseModel):

    def fields(self):
        return self._fields

    def remove(self):
        pipe = self.redis.pipeline()
        self.clean(pipe)
        self._session.add(self.cursor.items, None)
        pipe.execute()

    def incr(self, sect, key, val=1):
        section = getattr(self, sect)
        if not section.get(key):
            section[key] = val
        else:
            section[key] += val

    def decr(self, sect, key, val=1):
        section = getattr(self, sect)
        section[key] -= val
        if not section.get(key):
            section.remove(key)
