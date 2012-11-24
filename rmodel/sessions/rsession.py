# coding: utf8

from rmodel.sessions.base_session import BaseSession


class RSession(BaseSession):

    def __init__(self):
        self._store = []

    def add(self, items, value):
        self._store.append((items, value))

    def append(self, items, values, end):
        keys = xrange(end - len(values), end)
        self._store.append((items, dict(zip(keys, values))))

    def _get_nested(self, store, path):
        d = store
        for item in path:
            d.setdefault(item, {})
            d = d.get(item)

        return d

    def _save_change(self, nested, field, change):
        nested[field] = change

    def changes(self):
        rt = {}
        for items, change in self._store:
            items, last = items[:-1], items[-1]

            nested = self._get_nested(rt, items)
            self._save_change(nested, last, change)

        return rt
