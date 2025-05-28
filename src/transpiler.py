# transpiler.py
from llvmlite import ir
from src.nodes import *

class IrTranspiler:
    def __init__(self):
        self.type_map: dict[str, ir.type] = {
            'int' : ir.IntType(32)
        }

        self.module: ir.module = ir.Module('main')
        self.builder: ir.IRBuilder = ir.IRBuilder()

    def transpile(self, node: Stmt):
        match node.type:
            case 'Program':
                self.tp_program(node)

            case 'BinaryExpr':
                self.tp_binary_expr(node)
            

# region Statements  
    def tp_program(self, node: Program):
        func_name: str = 'main'
        param_types: list[ir.Type] = []
        return_type: ir.Type = self.type_map['int']

        fnty = ir.FunctionType(return_type, param_types)
        func = ir.Function(self.module, fnty, name=func_name)

        block = func.append_basic_block(f"{func_name}_entry")

        self.builder = ir.IRBuilder(block)

        for stmt in node.body:
            self.transpile(stmt)  # Also fix: was `self.transpile(node)`, which was wrong

        return_val: ir.Constant = ir.Constant(self.type_map['int'], 69)
        self.builder.ret(return_val)

# endregion


# region Expressions  
    def tp_binary_expr(self, node: BinaryExpr):
        op: str = node.op
        left_value, left_type = self.resolve_value(node.left)
        right_value, right_type = self.resolve_value(node.right)

        value = None
        Type= None
        if isinstance(right_type, ir.IntType) and isinstance(left_type, ir.IntType):
            Type = self.type_map['int']
            match op:
                case '+':
                    value = self.builder.add(left_value, right_value)
                case '-':
                    value = self.builder.sub(left_value, right_value)
                case '*':
                    value = self.builder.mul(left_value, right_value)
                case '/':
                    value = self.builder.sdiv(left_value, right_value)

        return value, Type

# endregion



# region Helper Methods
    def resolve_value(
        self, node: Expr, value_type: str = None) -> tuple[ir.Value, ir.Type]:
        match node.type:
            case 'NumericLiteral':
                node: NumericLiteral = node
                value, Type = node.value, self.type_map['int' if value_type is None else value_type]
                return ir.Constant(Type, value), Type
            
            case 'BinaryExpr':
                return self.tp_binary_expr(node)
            
# endregion

class CTranspiler:
    def __init__(self):
        self.code = []

    def transpile(self, node: Stmt):
        match node.type:
            case 'Program':
                self.tp_program(node)
            case 'BinaryExpr':
                return self.tp_binary_expr(node)

    def tp_program(self, node: Program):
        self.code.append("int main() {")
        for stmt in node.body:
            self.transpile(stmt)
        self.code.append("    return 69;")
        self.code.append("}")

    def tp_binary_expr(self, node: BinaryExpr):
        left, _ = self.resolve_value(node.left)
        right, _ = self.resolve_value(node.right)
        op = node.op
        expr = f"    int temp = {left} {op} {right};"
        self.code.append(expr)

    def resolve_value(self, node: Expr):
        match node.type:
            case 'NumericLiteral':
                return str(node.value), 'int'
            case 'BinaryExpr':
                # Could expand to nested expressions
                left, _ = self.resolve_value(node.left)
                right, _ = self.resolve_value(node.right)
                return f"({left} {node.op} {right})", 'int'  