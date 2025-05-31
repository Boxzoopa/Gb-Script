# transformer.py
from src.ir_nodes import *
from src.nodes import *

def ast_to_ir(node):
    match node.type:
        case "Program":
            return IRProgram([ast_to_ir(stmt) for stmt in node.body])

        case "Identifier":
            return IRIdent(node.value)

        case "NumericLiteral" | "StringLiteral":
            return IRConst(node.value)
        
        case "NullLiteral":
            return IRNull()
        
        case "Property":
            return IRProperty(node.name, node.d_type)
        
        case "IndexLiteral":
            return IRIndex(node.index, node.value)
        
        case "VariableDeclaration":
            return IRVarDecl(node.name, infer_type(node), node.is_const, ast_to_ir(node.value))
        
        case "ObjectDeclaration":
            props = []
            for prop in node.properties: props.append(ast_to_ir(prop))
            return IRObjDecl(node.name, props)
        
        case "GroupDeclaration":
            items = []
            for item in node.items:
                items.append(ast_to_ir(item))  # Transform AST IndexLiteral → IRIndex
            return IRGrpDecl(node.name, node.declared_type, node.size, items)

        case "FunctionDeclaration":
            stmts = []
            for stmt in node.body: stmts.append(ast_to_ir(stmt))
            args = []
            for arg in node.params: args.append(ast_to_ir(arg))
            return IRFuncDecl(node.name, args, node.return_type, stmts)

        case "StateDeclaration":
            stmts = []
            for stmt in node.body: stmts.append(ast_to_ir(stmt))
            return IRState(node.name, stmts)
        
        case "IfStmt":
            conds = []
            for cond in node.conditions: conds.append(ast_to_ir(cond))
            then = []
            for stmt in node.then_branch: then.append(ast_to_ir(stmt))
            elif_brnch = []
            for stmt in node.elif_branches: elif_brnch.append(ast_to_ir(stmt))
            else_brnch = []
            for stmt in node.else_branch: else_brnch.append(ast_to_ir(stmt))
            return IRIf(conds, then, elif_brnch, else_brnch)
        
        case "WhileStmt":
            cond = ast_to_ir(node.condition)
            stmts = []
            for stmt in node.body: stmts.append(ast_to_ir(stmt))
            return IRWhile(cond, stmts)

        case "ForStmt":
            init = ast_to_ir(node.init)
            cond = ast_to_ir(node.condition)
            inc = ast_to_ir(node.increment)
            stmts = []
            for stmt in node.body: stmts.append(ast_to_ir(stmt))
            return IRFor(init, cond, inc, stmts)

        case "ReturnStmt":
            return IRReturn(ast_to_ir(node.value))

        case "BinaryExpr":
            left_ir = ast_to_ir(node.left)
            right_ir = ast_to_ir(node.right)
            return IRBinary(node.op, left_ir, right_ir)
        
        case "UnaryExpr":
            return IRUnary(node.op, ast_to_ir(node.right), node.postfix)
        
        case "AssignmentExpr":
            return IRAssignment(node.assignee, ast_to_ir(node.value), node.op)
        
        case "CallExpr":
            args = []
            args = [ast_to_ir(arg) for arg in node.args]
            return IRCall(ast_to_ir(node.caller), args)
        
        case "MemberExpr":
            return IRMember(ast_to_ir(node.object), ast_to_ir(node.property), node.computed)


        case "ModuleNode":
            return IRModule(node.value)

        case _:
            raise NotImplementedError(f"AST node type '{node.type}' not supported.")
        
def infer_type(node):
    if hasattr(node, "explicit_type"):
        if node.explicit_type not in (None, "object"):
            return node.explicit_type
    
    match node.value.type:
        case "NumericLiteral" | "BinaryExpr" | "UnaryExpr":
            return "int"
    
        case "StringLiteral":
            return "str"
        
        case "Indentifier" | "NullLiteral":
            return "auto"

        case "ObjectLiteral":
            et = node.value
            node.value = NullLiteral()
            return f"{et}"
        
    return "auto"
    
def print_ir(node, indent=0):
    prefix = ' ' * indent
    if isinstance(node, IRProgram):
        print(prefix + "Program:")
        for stmt in node.body:
            print_ir(stmt, indent + 2)
    elif isinstance(node, IRFuncDecl):
        print(f"{prefix}Function {node.name}({', '.join(arg.name for arg in node.args)}):")
        for stmt in node.body:
            print_ir(stmt, indent + 2)
    elif isinstance(node, IRVarDecl):
        print(f"{prefix}Var {node.name} ({node.var_type}) = {node.value}")
    elif isinstance(node, IRGrpDecl):
        print(f"{prefix}Group {node.name}[{node.size}] ({node.var_type}):")
        for item in node.items:
            print_ir(item, indent + 2)
    elif isinstance(node, IRIndex):
        print(f"{prefix}[{node.index}] = {node.value}")
    elif isinstance(node, IRCall):
        print(f"{prefix}Call {node.func}({', '.join(str(arg) for arg in node.args)})")
    elif isinstance(node, IRBinary):
        print(f"{prefix}{node.left} {node.op} {node.right}")
    elif isinstance(node, IRUnary):
        print(f"{prefix}{node.op}{node.right}")
    elif isinstance(node, IRAssignment):
        print(f"{prefix}{node.assignee} {node.op} {node.value}")
    elif isinstance(node, IRReturn):
        print(f"{prefix}Return {node.value}")
    else:
        print(f"{prefix}{node}")

    
sprite_id_map = {}
next_sprite_id = 0

def assign_sprite_id(source):
    global next_sprite_id
    if source not in sprite_id_map:
        sprite_id_map[source] = next_sprite_id
        next_sprite_id += 1
    return sprite_id_map[source]
