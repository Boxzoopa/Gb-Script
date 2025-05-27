# eval.py
from src.nodes import *
from src.eval.context import *

class Evaluator:
    def __init__(self):
        self.ctx = Context()

    def evaluate(self, ast):
        if ast.type != "Program":
            raise EvaluationError("AST root node must be a Program")
        
        for node in ast.body:  # access .body attribute
            self.eval_stmt(node)
        
        print(self.ctx.to_dict())

    def eval_stmt(self, node):
        t = node.type
        match t:
            case 'VariableDecleration':
                self.eval_var_decl(node)

            case 'AssignmentExpr':
                self.eval_assignment(node)

            
            case _:
                raise EvaluationError(f"Uknown Statement Type: {t}")
            
    def eval_var_decl(self, node):
        name = node.name
        explicit_type = node.explicit_type  # Could be None
        is_const = node.is_const
        value_node = node.value

        if explicit_type == None:
            explicit_type = self.eval_expr(value_node)

        value_type = self.eval_expr(value_node)

        if explicit_type is not None and explicit_type != value_type:
            raise EvaluationError(f"Type mismatch: declared {explicit_type}, but value is {value_type}")

        var_type = explicit_type if explicit_type is not None else value_type

        self.ctx.declare_var(name, var_type, is_const)  


    def eval_assignment(self, node):
        assignee = node.assignee.value  # Assuming simple identifier
        if not self.ctx.has_var(assignee):
            raise EvaluationError(f"Assignment to undeclared variable `{assignee}`")
        
        var_type, is_const = self.ctx.get_var(assignee)
        if is_const:
            raise EvaluationError(f"Cannot assign to constant variable `{assignee}`")

        value_type = self.eval_expr(node.value)
        if var_type != value_type:
            raise EvaluationError(f"Type mismatch on assignment: variable `{assignee}` is {var_type}, assigned {value_type}")



    def eval_expr(self, node):
        t = node.type
        match t:
            case 'NumericLiteral':
                return 'int'
            
            case 'StringLiteral':
                return 'str'
            
            case 'Identifier':
                name = node.value
                if not self.ctx.has_var(name):
                    raise EvaluationError(f"Use of undeclared variable `{name}`")
                var_type, _ = self.ctx.get_var(name)
                return var_type
            
            case 'BinaryExpr':
                return 'int'
            
            case 'NullLiteral':
                return 'null'
            
            case _:
                raise EvaluationError(f"Unknown expression type: {t}")