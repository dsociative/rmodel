# coding: utf8

from rmodel.sessions.base_session import BaseSession


class RSession(BaseSession):

    def flush(self):
        self._store = {}

    def __init__(self):
        self.flush()

    def pop(self):
        changes = self.changes()
        self.flush()
        return changes

    def add(self, items, value):
        self.set_by_path(items, value)

    def append(self, items, values, end):
        keys = xrange(end - len(values), end)
        for key, value in zip(keys, values):
            self.add(items + (key,), value)

    def changes(self):
        return self._store

    def set_by_path(self, path, value):
        area, destination = self.pave_path(path)
        area[destination] = value

    def path_destination(self, path):
        return path[:-1], path[-1]

    def pave_path(self, path):
        area_path, destination  = self.path_destination(path)

        area = self._store
        for part in area_path:
            if area.get(part, None) is None:
                area[part] = {}

            area = area[part]
        return area, destination
