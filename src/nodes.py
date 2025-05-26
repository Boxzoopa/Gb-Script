# nodes.py
from typing import List

# Base Node Classes
class Stmt:
    def __init__(self, type):
        self.type = type

    def to_dict(self):
        return {
            "type": self.type
        }

class Program(Stmt):
    def __init__(self, body=None):
        super().__init__(type="Program")
        self.body : List[Stmt] = body if body is not None else []

    def to_dict(self):
        return {
            "type": "Program",
            "body": [stmt.to_dict() for stmt in self.body]
        }


class Expr(Stmt):
    def __init__(self):
        pass


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
