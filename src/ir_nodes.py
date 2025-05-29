# ir_nodes.py

class IRNode:
    def __init__(self):
        self.op = None

    def __repr__(self):
        return f"{self.__class__.__name__}()"
    
    def pretty(self, indent=0):
        pad = " " * indent
        cls_name = self.__class__.__name__
        result = f"{pad}{cls_name}"

        # Show only fields that aren't 'op' or private
        fields = [
            (name, getattr(self, name))
            for name in vars(self)
            if not name.startswith("_") and name != "op"
        ]

        for name, value in fields:
            if isinstance(value, IRNode):
                result += f"\n{value.pretty(indent + 2)}"
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, IRNode):
                        result += f"\n{item.pretty(indent + 2)}"
                    else:
                        result += f"\n{' ' * (indent + 2)}{repr(item)}"
            else:
                result += f"\n{' ' * (indent + 2)}{name}: {repr(value)}"

        return result

class IRProgram(IRNode):
    def __init__(self, body):
        super().__init__()
        self.op = "program"
        self.body = body  # List of IRNodes

    def __repr__(self):
        return f"IRProgram({self.body})"

class IRConst(IRNode):
    def __init__(self, value):
        super().__init__()
        self.op = "const"
        self.value = value

    def __repr__(self):
        return f"IRConst({self.value})"

class IRProperty(IRNode):
    def __init__(self, name, declared_type):
        super().__init__()
        self.op = "prop"
        self.name = name
        self.declared_type = declared_type

    def __repr__(self):
        return f"IRProperty({self.name}, {self.declared_type})"

class IRIndex(IRNode):
    def __init__(self, index, value):
        super().__init__()
        self.op = "index"
        self.index = index
        self.value = value
    
    def __repr__(self):
        return f"IRIndex({self.index}, {self.value})"

class IRVarDecl(IRNode):
    def __init__(self, name, explicit_type, is_const, value):
        super().__init__()
        self.op = "var_decl"
        self.name = name 
        self.explicit_type = explicit_type
        self.is_const = is_const
        self.value = value

    def __repr__(self):
        if self.is_const:
            return f"IRVarDecl('{self.name}', {self.explicit_type}, 'constant', {self.value})"
        else:
            return f"IRVarDecl('{self.name}', {self.explicit_type}, {self.value})"

class IRObjDecl(IRNode):
    def __init__(self, name, properties):
        super().__init__()
        self.op = "obj_decl"
        self.name = name
        self.properties = properties
    
    def __repr__(self):
        return f"IRObjDecl('{self.name}, {self.properties})"

class IRGrpDecl(IRNode):
    def __init__(self, name, declared_type, size, items):
        super().__init__()
        self.op = "grp_decl"
        self.name = name
        self.declared_type = declared_type
        self.size = size
        self.items = items  
        
    def __repr__(self):
        return f"IRGrpDecl({self.name}, {self.declared_type}, {self.size}, items({self.items}))"

class IRFuncDecl(IRNode):
    def __init__(self, name, params, return_type, body):
        super().__init__()
        self.op = "func_decl"
        self.name = name
        self.params = params  # List of IRProperty
        self.return_type = return_type
        self.body = body      # List of IRNodes

    def __repr__(self):
        return f"IRFuncDecl({self.name}, {self.return_type}, params({self.params}), body({self.body}))"

class IRIf(IRNode):
    def __init__(self, conditions, then_branch, elif_branches, else_branch):
        super().__init__()
        self.op = "if"
        self.conditions = conditions 
        self.then_branch = then_branch  
        self.elif_branches = elif_branches 
        self.else_branch = else_branch 

    def __repr__(self):
        return f"IRIf({self.conditions}, then({self.then_branch}), elif({self.elif_branches}), else({self.else_branch}))"

class IRWhile(IRNode):
    def __init__(self, condition, body):
        super().__init__()
        self.op = "while"
        self.condition = condition
        self.body = body 

    def __repr__(self):
        return f"IRWhile({self.condition}, do({self.body}))"

class IRFor(IRNode):
    def __init__(self, init, condition, increment, body):
        super().__init__()
        self.op = "for"
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

    def __repr__(self):
        return f"IRFor({self.init}, {self.condition}, {self.increment}, do({self.body}))"

class IRReturn(IRNode):
    def __init__(self, value):
        super().__init__()
        self.op = "return"
        self.value = value

    def __repr__(self):
        return f"IRReturn({self.value})"


class IRBinary(IRNode):
    def __init__(self, operator, left, right):
        super().__init__()
        self.op = "binary"
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"IRBinary('{self.operator}', {self.left}, {self.right})"

class IRUnary(IRNode):
    def __init__(self, operator, operand, postfix=False):
        super().__init__()
        self.op = "unary"
        self.operator = operator
        self.operand = operand
        self.postfix = postfix

    def __repr__(self):
        if self.postfix == False:
            return f"IRUnary({self.operator}{self.operand})"
        else:
            return f"IRUnary({self.operand}{self.operator})"

class IRAssignment(IRNode):
    def __init__(self, assignee, value, operator):
        super().__init__()
        self.op = "assign"
        self.assignee = assignee  # IRIdentifier or IRMemberExpr
        self.value = value
        self.operator = operator

    def __repr__(self):
        return f"IRAssignment('{self.assignee}', {self.value}, {self.operator})"
    
class IRCall(IRNode):
    def __init__(self, caller, args):
        super().__init__()
        self.caller = caller
        self.args = args
    
    def __repr__(self):
        return f"IRCall({self.caller}, args({self.args}))"

class IRMember(IRNode):
    def __init__(self, obj, prop, computed=False):
        super().__init__()
        self.op = "member"
        self.object = obj
        self.property = prop
        self.computed = computed
    
    def __repr__(self):
        return f"IRMember({self.object}.{self.property}, {self.computed})"

