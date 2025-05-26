# nodes.py
from typing import List

# Base Node Classes
class Stmt:
    def __init__(self):
        pass

class Expr:
    def __init__(self):
        pass

# Statements
class ProgramStmt(Stmt):
    def __init__(self, body=None):
        super().__init__()
        self.body : List[Stmt] = body if body is not None else []

    def to_dict(self):
        return {
            "type": "ProgramStmt",
            "body": [stmt.to_dict() for stmt in self.body]
        }

    
class ExpressionStmt(Stmt):
    def __init__(self, body=None):
        super().__init__()
        self.expression : Expr = body if body is not None else None

    def to_dict(self):
        return {
            "type": "ExpressionStmt",
            "expression": self.expression.to_dict()
        }


# Expressions
## Literal Nodes
class NumberExpr(Expr):
    def __init__(self, value):
        super().__init__()
        self.value : float = value

    def to_dict(self):
        return {
            "type": "NumberExpr",
            "value": self.value
        }


class StringExpr(Expr):
    def __init__(self, value):
        super().__init__()
        self.value : str = value

    def to_dict(self):
        return {
            "type": "StringExpr",
            "value": self.value
        }

class SymbolExpr(Expr):
    def __init__(self, value):
        super().__init__()
        self.value : str = value

    def to_dict(self):
        return {
            "type": "SymbolExpr",
            "value": self.value
        }

## Complex Nodes
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
            "operator": self.op.kind  # or str(self.op)
        }
    

    

