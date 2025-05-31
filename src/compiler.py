#compiler
from llvmlite import ir

# Create LLVM context, module, builder
module = ir.Module(name="gbscript_module")
func_ty = ir.FunctionType(ir.IntType(32), [])
main_func = ir.Function(module, func_ty, name="main")
block = main_func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)

def compile_expr(node):
    if node["type"] == "NumericLiteral":
        return ir.Constant(ir.IntType(32), node["value"])

    elif node["type"] == "BinaryExpr":
        left_val = compile_expr(node["left"])
        right_val = compile_expr(node["right"])
        op = node["operator"]

        if op == "+":
            return builder.add(left_val, right_val, name="addtmp")
        elif op == "-":
            return builder.sub(left_val, right_val, name="subtmp")
        elif op == "*":
            return builder.mul(left_val, right_val, name="multmp")
        elif op == "/":
            return builder.sdiv(left_val, right_val, name="divtmp")
        else:
            raise Exception(f"Unknown operator {op}")

    else:
        raise Exception(f"Unknown node type {node['type']}")

# Compile the first statement in the program body
program = {
   "type": "Program",
   "body": [
      {
         "type": "BinaryExpr",
         "left": {
            "type": "BinaryExpr",
            "left": {
               "type": "NumericLiteral",
               "value": 5
            },
            "right": {
               "type": "NumericLiteral",
               "value": 5
            },
            "operator": "+"
         },
         "right": {
            "type": "NumericLiteral",
            "value": 10
         },
         "operator": "*"
      }
   ]
}

result = compile_expr(program["body"][0])
builder.ret(result)

print(module)
