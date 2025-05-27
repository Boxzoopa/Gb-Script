# nodes.py
from typing import List

class Stmt:
    def __init__(self, type):
        self.type = type

    def to_dict(self):
        return {
            "type": self.type
        }
    
class Expr(Stmt):
    def __init__(self):
        pass

# Statements
class Program(Stmt):
    def __init__(self, body=None):
        super().__init__(type="Program")
        self.body : List[Stmt] = body if body is not None else []

    def to_dict(self):
        return {
            "type": "Program",
            "body": [stmt.to_dict() for stmt in self.body]
        }

class VariableDecleration(Stmt):
    def __init__(self, name: str, value: Expr=None, is_const: bool = False, explicit_type=None):
        self.name = name
        self.value = value or NullLiteral() if value is None else value
        self.is_const = is_const
        self.explicit_type = explicit_type  # Placeholder for future type annotations

    def to_dict(self):
        return {
            "type": "VariableDecleration",
            "name": self.name,
            "explicit_type": self.explicit_type,
            "is_const": self.is_const,
            "value": self.value.to_dict()
        }

# Expressions
class Identifier(Expr):
    def __init__(self, value):
        super().__init__()
        self.value : str = value

    def to_dict(self):
        return {
            "type": "Identifier",
            "value": self.value
        }

class NumericLiteral(Expr):
    def __init__(self, value):
        super().__init__()
        self.value : int = value

    def to_dict(self):
        return {
            "type": "NumericLiteral",
            "value": self.value
        }

class StringLiteral(Expr):
    def __init__(self, value):
        super().__init__()
        self.value : str = value

    def to_dict(self):
        return {
            "type": "StringLiteral",
            "value": self.value
        }

class NullLiteral(Expr):
    def __init__(self):
        super().__init__()
        self.value = "null"

    def to_dict(self):
        return {
            "type": "NullLiteral",
            "value": self.value
        }
    
class BinaryExpr(Expr):
    def __init__(self, left, right, op):
        super().__init__()
        self.left = left
        self.right = right
        self.op = op

    def to_dict(self):
        return {
            "type": "BinaryExpr",
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
            "operator": self.op  # or str(self.op)
        }
