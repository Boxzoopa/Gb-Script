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
        self.type = "Program"
        self.body : List[Stmt] = body if body is not None else []

    def to_dict(self):
        return {
            "type": "Program",
            "body": [stmt.to_dict() for stmt in self.body]
        }

class VariableDeclaration(Stmt):
    def __init__(self, name: str, value: Expr=None, is_const: bool = False, explicit_type=None):
        self.type = "VariableDeclaration"
        self.name = name
        self.value = value or NullLiteral() if value is None else value
        self.is_const = is_const
        self.explicit_type = explicit_type  # Placeholder for future type annotations

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "explicit_type": self.explicit_type,
            "is_const": self.is_const,
            "value": self.value.to_dict()
        }

class GroupDeclaration(Stmt):
    def __init__(self, name, _type, size=0, items=None):
        self.type = "GroupDeclaration"
        self.name = name
        self.declared_type = _type
        self.size = size
        self.items = items

    def to_dict(self):
        return {
            "type": "GroupDeclaration",
            "name": self.name,
            "declared_type": self.declared_type,
            "size": self.size,
            "items": [item.to_dict() for item in self.items]  # Assuming items will be added later
        }

class Property:
    def __init__(self, name: str, type: str):
        self.type = "Property"
        self.name = name
        self.d_type = type

    def to_dict(self):
        return {
            "type": "Property",
            "name": self.name,
            "declared_type": self.d_type
        }
    
class ObjectDeclaration(Stmt):
    def __init__(self, name: str, properties: List[Property]):
        self.type="ObjectDeclaration"
        self.name = name
        self.properties = properties


    def props_to_dict(self):
        props = []
        for prop in self.properties:
            props.append(prop.to_dict())
        return props

    def to_dict(self):
        return {
            "type": "ObjectDeclaration",
            "name": self.name,
            "properties": self.props_to_dict()
        }

class FunctionDeclaration(Stmt):
    def __init__(self, name: str, params: List[Property],
                 body: List[Stmt], return_type: str = None):
        self.type = "FunctionDeclaration"
        self.name = name
        self.params = params
        self.return_type = return_type if return_type is not None else "void"
        self.body = body if body is not None else []
    
    def to_dict(self):
        return {
            "type": "FunctionDeclaration",
            "name": self.name,
            "params": [param.to_dict() for param in self.params],
            "return_type": self.return_type,
            "body": [stmt.to_dict() for stmt in self.body]
        }

class StateDeclaration(Stmt):
    def __init__(self, name: str, body: List[Stmt]):
        self.type = "StateDeclaration"
        self.name = name
        self.body = body if body is not None else []
    
    def to_dict(self):
        return {
            "type": "StateDeclaration",
            "name": self.name,
            "body": [stmt.to_dict() for stmt in self.body]
        }

class ReturnStmt(Stmt):
    def __init__(self, value=None):
        self.value = value or NullLiteral()  # Default to null if no value is provided
        self.type = "ReturnStmt"

    def to_dict(self):
        return {
            "type": "ReturnStmt",
            "value": self.value.to_dict()
        }
    
class IfStmt(Stmt):
    def __init__(self, conditions, then_branch, elif_branches=None, else_branch=None):
        self.type = "IfStmt"
        self.conditions = conditions
        self.then_branch = then_branch
        self.elif_branches = elif_branches if elif_branches is not None else []
        self.else_branch = else_branch if else_branch is not None else []

    def to_dict(self):
        return {
            "type": "IfStmt",
            "conditions": [cond.to_dict() for cond in self.conditions],
            "then_branch": [stmt.to_dict() for stmt in self.then_branch],
            "elif_branches": [stmt.to_dict() for stmt in self.elif_branches],
            "else_branch": [stmt.to_dict() for stmt in self.else_branch]
        }
    
class WhileStmt(Stmt):
    def __init__(self, condition, body):
        self.type = "WhileStmt"
        self.condition = condition
        self.body = body

    def to_dict(self):
        return {
            "type": "WhileStmt",
            "condition": self.condition.to_dict(),
            "body": [stmt.to_dict() for stmt in self.body]
        }
    
class ForStmt(Stmt):
    def __init__(self, init, condition, increment, body):
        self.type = "ForStmt"
        self.init = init  # Typically a VariableDecleration or AssignmentExpr
        self.condition = condition
        self.increment = increment  # Usually an AssignmentExpr
        self.body = body

    def to_dict(self):
        return {
            "type": "ForStmt",
            "init": self.init.to_dict(),
            "condition": self.condition.to_dict(),
            "increment": self.increment.to_dict(),
            "body": [stmt.to_dict() for stmt in self.body]
        }



# Expressions
class Identifier(Expr):
    def __init__(self, value):
        self.type = "Identifier"
        self.value : str = value

    def to_dict(self):
        return {
            "type": "Identifier",
            "value": self.value
        }
    
    def __repr__(self):
        return f"{self.value}"

class NumericLiteral(Expr):
    def __init__(self, value):
        self.type = "NumericLiteral"
        self.value : int = value

    def to_dict(self):
        return {
            "type": "NumericLiteral",
            "value": self.value
        }
    
    def __repr__(self):
        return f"{self.value}"

class StringLiteral(Expr):
    def __init__(self, value):
        self.type = "StringLiteral"
        self.value : str = value

    def to_dict(self):
        return {
            "type": "StringLiteral",
            "value": self.value
        }
        
    def __repr__(self):
        return f"'{self.value}'"

class NullLiteral(Expr):
    def __init__(self):
        self.type = "NullLiteral"
        self.value = "null"

    def to_dict(self):
        return {
            "type": "NullLiteral",
            "value": self.value
        }
     
    def __repr__(self):
        return "undefined"
    
class IndexLiteral(Expr):
    def __init__(self, index, value):
        super().__init__()
        self.type = "IndexLiteral"
        self.index = index
        self.value = value

    def to_dict(self):
        return {
            "type": "IndexLiteral",
            "index": self.index,
            "value": self.value.to_dict()
        }
    
    def __repr__(self):
        return f"{self.index}, {self.value}"

class ObjectLiteral(Expr):
    def __init__(self, name: str):
        self.type="ObjectLiteral"
        self.struct_name = name

    def to_dict(self):
        return {
            "type": "ObjectLiteral",
            "struct_name": self.struct_name
        }
    
    def __repr__(self):
        return f"{self.struct_name}"
    
class BinaryExpr(Expr):
    def __init__(self, left, right, op):
        self.type = "BinaryExpr"
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
    
    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

class UnaryExpr(Expr):
    def __init__(self, right, op, postfix=False):
        self.type = "UnaryExpr"
        self.right = right
        self.op = op
        self.postfix = postfix

    def to_dict(self):
        return {
            "type": "UnaryExpr",
            "operator": self.op,  # or str(self.op)
            "right": self.right.to_dict(),
            "postfix": self.postfix
        }
    
    def __repr__(self):
        return f"{self.op}{self.right}" 
    
class AssignmentExpr(Expr):
    def __init__(self, assignee, value, op="="):
        super().__init__()
        self.type = "AssignmentExpr"
        self.assignee = assignee # +=, =, -=, 
        self.value = value
        self.op = op

    def to_dict(self):
        return {
            "type": self.type,
            "assignee": self.assignee.to_dict(),
            "value": self.value.to_dict(),
            "operator": self.op
        }

class CallExpr(Expr):
    def __init__(self, caller, args = List[Expr]):
        self.type = "CallExpr"
        self.caller = caller
        self.args = args

    def to_dict(self):
        return {
            "type": "CallExpr",
            "caller": self.caller.to_dict(),
            "args": [arg.to_dict() for arg in self.args]
        }
    
    def __repr__(self):
        return f"{self.caller}({', '.join(map(str, self.args))})"

class MemberExpr(Expr):
    def __init__(self, object, property, computed=False):
        self.type ="MemberExpr"
        self.object = object
        self.property = property
        self.computed = computed  # Default to dot notation

    def to_dict(self):
        return {
            "type": "MemberExpr",
            "object": self.object.to_dict(),
            "property": self.property.to_dict(),
            "computed": self.computed
        }
    
    def __repr__(self):
        if self.computed == False:
            return f"{self.object}.{self.property}"
        else:
            return f"{self.object}[{self.property}]"


class ModuleNode(Expr):
    def __init__(self, value):
        self.type = "ModuleNode"
        self.value : str = value

    def to_dict(self):
        return {
            "type": "ModuleNode",
            "value": self.value
        }
        
    def __repr__(self):
        return f"'{self.value}'"