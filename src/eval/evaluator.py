# eval.py
from src.nodes import *
from src.eval.context import *

class Evaluator:
    def __init__(self):
        self.ctx = Context()
        self.last_value = None


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

            case 'ObjectDeclaration':
                self.eval_object_decl(node)

            case 'GroupDecleration':
                self.eval_group_decl(node)

            case 'MemberExpr':
                self.eval_expr(node)
            
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

        # If the evaluated value is a constructed object, store the actual instance
        actual_value = self.last_value if self.last_value is not None else value_type

       # Allow any object type if declared type is 'object'
        if explicit_type == "object" and isinstance(value_type, str) and self.ctx.is_object_type(value_type):
            pass  # Accept it
        elif explicit_type is not None and explicit_type != value_type and value_type != 'null':
            raise EvaluationError(f"Type mismatch: declared {explicit_type}, but value is {value_type}")


        var_type = explicit_type if explicit_type is not None else value_type
        self.ctx.declare_var(name, var_type, is_const)
        self.ctx.set_var_value(name, actual_value)
        self.last_value = None

    def eval_group_decl(self, node):
        name = node.name
        element_type = node.declared_type
        declared_size = int(node.size)
        items = [self.eval_expr(item.value) for item in node.items]
        
        for i, item_type in enumerate(items):
            if item_type != element_type:
                raise EvaluationError(f"Type mismatch at index {i}: expected {element_type}, got {item_type}")

        if len(items) > declared_size:
            raise EvaluationError(f"Too many initializers for `{name}`: declared size is {declared_size}")
        
        self.ctx.declare_var(name, f"{element_type}[]", is_const=False)
        self.ctx.set_group_items(name, items)  # custom method to store items
    
    def eval_object_decl(self, node):
        self.ctx.declare_object_type(node.name, {prop.name: prop.type for prop in node.properties})


    def eval_assignment(self, node):
        assignee = node.assignee.value  # Assuming simple identifier
        if node.assignee.type == 'Identifier':
            if not self.ctx.has_var(assignee):
                raise EvaluationError(f"Assignment to undeclared variable `{assignee}`")
            
            var_type, is_const = self.ctx.get_var(assignee)
            if is_const:
                raise EvaluationError(f"Cannot assign to constant variable `{assignee}`")

            value_type = self.eval_expr(node.value)
            if var_type != value_type:
                raise EvaluationError(f"Type mismatch on assignment: variable `{assignee}` is {var_type}, assigned {value_type}")

        elif node.assignee.type == 'MemberExpr':
            self.eval_member_assignment(node)
        else:
            raise EvaluationError("Unsupported assignment target")

    def eval_member_assignment(self, node):
        obj_name = node.assignee.object.value
        field_name = node.assignee.property.value
        value_type = self.eval_expr(node.value)

        val = self.ctx.get_var_value(obj_name)
        if not isinstance(val, dict) or '__type__' not in val:
            raise EvaluationError(f"{obj_name} is not an object")

        obj_type = val['__type__']
        field_types = self.ctx.get_object_type(obj_type)

        expected_type = field_types.get(field_name)
        if not expected_type:
            raise EvaluationError(f"Field `{field_name}` not declared on `{obj_type}`")

        if expected_type != value_type:
            raise EvaluationError(f"Type mismatch for `{obj_name}.{field_name}`: expected {expected_type}, got {value_type}")

        val['fields'][field_name] = value_type  # Or actual value if tracking values

    def eval_call_expr(self, node):
        if node.caller.type == 'MemberExpr':
            obj = node.caller.object.value  # e.g., Rect
            prop = node.caller.property.value  # e.g., new
            if prop == 'new':
                obj_def = self.ctx.get_object_type(obj)
                instance_fields = {k: None for k in obj_def}
                instance = {'__type__': obj, 'fields': instance_fields}
                self.last_value = instance
                return 'object'


        raise EvaluationError("Unsupported function call")


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
            
            case 'UnaryExpr':
                return 'int'
            
            case 'NullLiteral':
                return 'null'

            case 'MemberExpr':
                return self.eval_expr(node)  # Allows member reads like `square.width`

            case 'CallExpr':
                return self.eval_call_expr(node)
            
            case 'MemberExpr' if node.computed:
                obj = node.object.value
                idx_type = self.eval_expr(node.property)
                if idx_type != 'int':
                    raise EvaluationError(f"Index must be int, got {idx_type}")
                
                var_type, _ = self.ctx.get_var(obj)
                if not var_type.endswith("[]"):
                    raise EvaluationError(f"Cannot index non-group variable `{obj}`")
                return var_type[:-2]  # 'int[]' -> 'int'
                        
            case _:
                raise EvaluationError(f"Unknown expression type: {t}")