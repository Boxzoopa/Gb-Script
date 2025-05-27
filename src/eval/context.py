# context.py

class EvaluationError(Exception):
    pass

class Context:
    def __init__(self):
        self.variables = {}     # name -> (type, is_const)
        self.values = {}        # name -> actual value (list, object, int, etc.)

        self.object_types = {}  # e.g., 'Rect': {'width': 'int', 'height': 'int'}


    def declare_var(self, name, type, is_const):
        if name in self.variables:
            raise EvaluationError(f"Variable `{name}` already declared")
        self.variables[name] = (type, is_const)
        self.values[name] = None  # Default value


    def set_var_value(self, name, value):
        if name not in self.variables:
            raise EvaluationError(f"Variable `{name}` is not declared")
        _, is_const = self.variables[name]
        if is_const and self.values[name] is not None:
            raise EvaluationError(f"Cannot reassign to constant `{name}`")
        self.values[name] = value

    def get_var_value(self, name):
        if name not in self.values:
            raise EvaluationError(f"Variable `{name}` has no value")
        return self.values[name]

    def get_var(self, name):
        return self.variables.get(name)

    def has_var(self, name):
        return name in self.variables


    def declare_object_type(self, name, fields):
        if name in self.object_types:
            raise EvaluationError(f"Object `{name}` already declared")
        self.object_types[name] = fields  # dict: field_name -> type

    def get_object_type(self, name):
        if name not in self.object_types:
            raise EvaluationError(f"Object `{name}` is not defined")
        return self.object_types[name]

    def set_group_items(self, name, items):
        if name not in self.variables:
            raise EvaluationError(f"Group `{name}` not declared")
        self.values[name] = items

    def is_object_type(self, typename):
        return typename in self.object_types



    def to_dict(self):
        return {
            name: {
                'type': self.variables[name][0],
                'const': self.variables[name][1],
                'value': self.values.get(name)
            }
            for name in self.variables
        }

