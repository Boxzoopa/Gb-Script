# transformer.py
from src.ir_nodes import *
from src.nodes import *

def ast_to_ir(node):
    match node.type:
        case "Program":
            return IRProgram([ast_to_ir(stmt) for stmt in node.body])

        case "NumericLiteral" | "StringLiteral" | "Identifier":
            return IRConst(node.value)
        
        case "Property":
            return IRProperty(node.name, node.d_type)
        
        case "IndexLiteral":
            return IRIndex(node.index, node.value)
        
        case "VariableDeclaration":
            return IRVarDecl(node.name, infer_type(node), node.is_const, node.value)
        
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
            return IRReturn(node.value)

        case "BinaryExpr":
            left_ir = ast_to_ir(node.left)
            right_ir = ast_to_ir(node.right)
            return IRBinary(node.op, left_ir, right_ir)
        
        case "UnaryExpr":
            return IRUnary(node.op, node.right, node.postfix)
        
        case "AssignmentExpr":
            return IRAssignment(node.assignee, node.value, node.op)
        
        case "CallExpr":
            args = []
            for arg in node.args: args.append(ast_to_ir(arg))
            return IRCall(node.caller.value, node.args)
        
        case "MemberExpr":
            pass

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
    
    
    
