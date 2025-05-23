# nodes.py

class ProgramNode:
    def __init__(self, body):
        self.body = body

    def to_dict(self):
        return {"type": "program", "body": self.body}

class NumberNode:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {"type": "number", "value": self.value}

    
class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def to_dict(self):
        return {"type": "binary_op", "left": self.left, "operator": self.operator, "right": self.right}


class UnaryOpNode:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def to_dict(self):
        return {"type": "unary_op", "operator": self.operator, "operand": self.operand}
    

class ExpressionNode:
    def __init__(self, expression):
        self.expression = expression

    def to_dict(self):
        return {"type": "expression", "expression": self.expression}
    
class GroupedNode:
    def __init__(self, expression):
        self.expression = expression

    def to_dict(self):
        return {"type": "grouped", "expression": self.expression}

class StringNode:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "type": "string",
            "value": self.value
        }


class VarDeclNode:
    def __init__(self, name, value, is_const, type_):
        self.name = name
        self.value = value
        self.is_const = is_const
        self.type = type_

    def to_dict(self):
        return {
            "type": "var_decl",
            "name": self.name,
            "value": self.value,
            "is_const": self.is_const,
            "var_type": self.type,
        }



class GrpDeclNode:
    def __init__(self, name, values, type_):
        self.name = name
        self.values = values
        self.type = type_

    def to_dict(self):
        return {
            "type": "group_decl",
            "group_type": self.type,
            "name": self.name,
            "values": self.values,
        }

class IndexNode:
    def __init__(self, group, index: int, value):
        self.group = group
        self.index = index
        self.value = value

    def to_dict(self):
        return {
            "type": "index",
            "group": self.group,
            "index": self.index,
            "value": self.value,
        }