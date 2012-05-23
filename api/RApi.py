# coding: utf8

SET = ' set '

class RApi(object):


    def __call__(self, root, query):

        if SET in query:
            select, action = query.split(SET)
        else:
            select, action = query, None

        return self.execute(root, select, action)


    def action(self, models, action):

        for model in models:
            fields, value = self.parse_select(action)

            if value.isdigit():
                value = int(value)

            end_field = fields.pop()
            for field in fields:
                model = getattr(model, field)

            setattr(model, end_field, value)


    def execute(self, root, select=None, action=None):

        models = self.find(root, select)

        if action:
            self.action(models, action)

        return [model.data() for model in models]


    def parse_select(self, select):
        models, value = select.split('=')
        return models.split('.'), value


    def find(self, root, select):
        rt = []

        fields, value = self.parse_select(select)

        for model in root.models:
            if self.end_value(model, fields) == value:
                rt.append(model)

        return rt

    def end_value(self, model, fields):
        rt = model

        for field in fields:
            rt = getattr(rt, field)

        return str(rt)
