# context.py

class EvaluationError(Exception):
    pass

class Context:
    def __init__(self):
        self.variables = {}

    def declare_var(self, name, type, is_const):
        if name in self.variables:
            raise EvaluationError(f"Variable `{name}` already declared")
        self.variables[name] = (type, is_const)

    def get_var(self, name):
        return self.variables.get(name)

    def has_var(self, name):
        return name in self.variables

    def to_dict(self):
        return self.variables.copy()
