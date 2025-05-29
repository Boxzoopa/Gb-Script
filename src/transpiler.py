# transpiler.py
from src.nodes import *
from src.ir_nodes import IRNode


class GBIRTranspiler:
    def __init__(self):
        self.ir = []

    def transpile(self, node):
        match node.type:
            case 'Program': return self.transpile_program(node)
            case 'NumericLiteral': return IRNode('const', [node.value])
            case 'StringLiteral': return IRNode('const', [f'"{node.value}"'])
            case 'NullLiteral': return IRNode('const', [node.value])
            case 'Identifier': return IRNode('ident', [node.value])
            case 'ObjectLiteral': return IRNode('const', [node.struct_name])

            case 'VariableDeclaration': return self.transpile_var_decl(node)
            case 'ObjectDeclaration': return self.transpile_object_decl(node)
            case 'GroupDeclaration': return self.transpile_group_decl(node)
            case 'FunctionDeclaration': return self.transpile_function_decl(node)

            case 'ReturnStmt': return IRNode('return', [self.transpile(node.value)])
            case 'IfStmt': return self.transpile_if_stmt(node)
            case 'WhileStmt': return self.transpile_while_stmt(node)
            case 'ForStmt': return self.transpile_for_stmt(node)

            case 'BinaryExpr':
                left = self.transpile(node.left)
                right = self.transpile(node.right)
                return IRNode(node.op, [left, right])
            case 'UnaryExpr':
                operand = self.transpile(node.right)
                return IRNode(node.op, [operand])
            case 'AssignmentExpr': return self.transpile_assignment_expr(node)
            case 'MemberExpr': return self.transpile_member_expr_ir(node)
            case 'CallExpr':
                caller_ir = self.transpile(node.caller)
                args_ir = [self.transpile(arg) for arg in node.args]
                return IRNode('call', [caller_ir] + args_ir)

            case _:
                raise NotImplementedError(f"Unsupported node type: {node.type}")

    def transpile_program(self, node):
        for stmt in node.body:
            self.ir.append(self.transpile(stmt))
        return self.ir

    def transpile_var_decl(self, node):
        value_ir = self.transpile(node.value) if node.value else IRNode("const", ["null"])
        ir = IRNode('var_decl' if not node.is_const else 'const_decl', [node.name, value_ir])

        if node.explicit_type != "null":
            ir.meta = {'explicit_type': node.explicit_type}

        if node.explicit_type == "object":
            ir.meta = {'explicit_type': node.value.struct_name}

        return ir

    def transpile_object_decl(self, node):
        props = [IRNode('struct_prop', [prop.name, prop.type]) for prop in node.properties]
        return IRNode('struct_decl', [node.name, props])

    def transpile_group_decl(self, node):
        items_ir = [IRNode('index', [item.index, self.transpile(item.value)]) for item in node.items]
        return IRNode('array_decl', [node.name, node.declared_type, int(node.size), items_ir])

    def transpile_function_decl(self, node):
        params = [IRNode('func_args', [p.name, p.type]) for p in node.params]
        body = [self.transpile(stmt) for stmt in node.body]
        return IRNode('func_decl', [node.name, node.return_type, params, body])

    def transpile_if_stmt(self, node):
        condition_ir = self.transpile(node.conditions[0]) if node.conditions else IRNode('const', ['true'])
        then_ir = [self.transpile(s) for s in node.then_branch]
        elifs_ir = [self.transpile_if_stmt(e) for e in node.elif_branches]
        else_ir = [self.transpile(s) for s in node.else_branch] if node.else_branch else []
        return IRNode('if', [condition_ir, then_ir, elifs_ir, else_ir])

    def transpile_while_stmt(self, node):
        condition_ir = self.transpile(node.condition)
        body_ir = [self.transpile(s) for s in node.body]
        return IRNode('while', [condition_ir, body_ir])

    def transpile_for_stmt(self, node):
        init_ir = self.transpile(node.init) if node.init else None
        cond_ir = self.transpile(node.condition) if node.condition else IRNode('const', ['true'])
        incr_ir = self.transpile(node.increment) if node.increment else None
        body_ir = [self.transpile(s) for s in node.body]
        return IRNode('for', [init_ir, cond_ir, incr_ir, body_ir])

    def transpile_assignment_expr(self, node):
        op = node.op
        value_ir = self.transpile(node.value)

        if node.assignee.type == 'Identifier':
            assignee = node.assignee.value
        elif node.assignee.type == 'MemberExpr':
            assignee = self.transpile_member_expr(node.assignee)
        else:
            raise NotImplementedError(f"Unsupported assignee type: {node.assignee.type}")

        match op:
            case '=': return IRNode('assign', [assignee, value_ir])
            case '+=' | "-=": return IRNode(op, [assignee, value_ir])
            case _: raise NotImplementedError(f"Unsupported assignment operator {op}")

    def transpile_member_expr(self, node):
        if node.type == "Identifier":
            return node.value
        if node.type == "MemberExpr":
            obj_str = self.transpile_member_expr(node.object)
            prop_str = node.property.value
            return f"{obj_str}.{prop_str}"
        raise NotImplementedError(f"Unsupported node type in member expression: {node.type}")

    def transpile_member_expr_ir(self, node):
        obj_ir = self.transpile(node.object)
        if node.computed:
            prop_ir = self.transpile(node.property)
            return IRNode('index', [obj_ir, prop_ir])
        return IRNode('member', [obj_ir, node.property.value])
