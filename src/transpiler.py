# transpiler.py
from src.ir_nodes import *

indent_level = 0
# Maps GBScript built-in functions to their C equivalents or wrapped functions
CALL_ALIASES = {
    "print": "gbs_print",
}


def generate_c(ir, indent_level=0):
    if isinstance(ir, IRProgram):
        stmts = []
        for stmt in ir.body:
            code = generate_c(stmt, indent_level)
            if code:  # skip empty/null
                stmts.append(get_indent(indent_level) + code + ";")
        return "\n".join(stmts)

    elif isinstance(ir, IRNull):
        return ""

    elif isinstance(ir, IRIdent):
        return str(ir.value)
        
    elif isinstance(ir, IRConst):
        if ir.value is None:
            return "NULL"
        elif isinstance(ir.value, str):
            return f"\"{ir.value}\""
        else:
            return str(ir.value)


    elif isinstance(ir, IRVarDecl):
        var_type = convert_type(ir.explicit_type) or "auto"
        const = "const " if ir.is_const else ""
        name = ir.name
        value_code = generate_c(ir.value) if not isinstance(ir.value, IRNull) else ""
        assign = f" = {value_code}" if value_code else ""
        return f"{const}{var_type} {name}{assign}"

    elif isinstance(ir, IRObjDecl):
        struct_lines = ["typedef struct {"]
        for prop in ir.properties:
            struct_lines.append(
                get_indent(indent_level + 1) + f"{generate_c(prop)};"
            )
        struct_lines.append(get_indent(indent_level) + f"}} {ir.name}")
        return "\n".join(struct_lines)
    
    elif isinstance(ir, IRGrpDecl):
        decl = f"{convert_type(ir.declared_type)} {ir.name}[{ir.size}]"

        if ir.items:
            size = int(ir.size)  # <-- fix: ensure it's an integer
            values = ["0"] * size  # default fallback
            for item in ir.items:
                idx = item.index
                val = generate_c(IRConst(item.value), indent_level)
                if 0 <= idx < size:
                    values[idx] = val

            initializer = "{" + ", ".join(values) + "}"
            return f"{decl} = {initializer}"
        else:
            return f"{decl}" 

    elif isinstance(ir, IRFuncDecl):
        decl = f"{ir.return_type} {ir.name}("
        decl += ", ".join(generate_c(p) for p in ir.params)
        decl += ") {\n"

        body_lines = [generate_c(stmt, indent_level + 1) + ";" for stmt in ir.body]
        body_code = "\n".join(indent_lines(body_lines, indent_level + 1))
        
        decl += body_code + "\n" + get_indent(indent_level) + "}"
        return decl


    elif isinstance(ir, IRIf):
        lines = []

        # Handle main if condition
        cond = generate_c(ir.conditions[0])
        lines.append(f"{get_indent(indent_level)}if ({cond}) {{")
        for stmt in ir.then_branch:
            lines.append(get_indent(indent_level + 1) + generate_c(stmt) + ";")
        lines.append(get_indent(indent_level) + "}")

        # Handle elif blocks
        for elif_ir in ir.elif_branches:
            # If it's a full nested IRIf, recurse into it and replace "if" with "else if"
            if isinstance(elif_ir, IRIf):
                elif_code = generate_c(elif_ir, indent_level)
                # Replace first 'if' with 'else if'
                elif_code = elif_code.replace("if", "else if", 1)
                lines.append(elif_code)
            else:
                elif_cond = generate_c(elif_ir.conditions[0])
                lines.append(f"{get_indent(indent_level)}else if ({elif_cond}) {{")
                for stmt in elif_ir.then_branch:
                    lines.append(get_indent(indent_level + 1) + generate_c(stmt) + ";")
                lines.append(get_indent(indent_level) + "}")

        # Handle else
        if ir.else_branch:
            if len(ir.else_branch) > 0:
                lines.append(f"{get_indent(indent_level)}else {{")
                for stmt in ir.else_branch:
                    lines.append(get_indent(indent_level + 1) + generate_c(stmt) + ";")
                lines.append(get_indent(indent_level) + "}")

        return "\n".join(lines)

    elif isinstance(ir, IRWhile):
        cond_code = generate_c(ir.condition)
        lines = [f"{get_indent(indent_level)}while ({cond_code}) {{"]

        for stmt in ir.body:
            stmt_code = generate_c(stmt, indent_level + 1)
            lines.append(get_indent(indent_level + 1) + stmt_code + ";")

        lines.append(get_indent(indent_level) + "}")
        return "\n".join(lines)

    elif isinstance(ir, IRFor):
        init_code = generate_c(ir.init)
        cond_code = generate_c(ir.condition)
        inc_code = generate_c(ir.increment)

        lines = [f"{get_indent(indent_level)}for ({init_code}; {cond_code}; {inc_code}) {{"]

        for stmt in ir.body:
            stmt_code = generate_c(stmt, indent_level + 1)
            lines.append(get_indent(indent_level + 1) + stmt_code + ";")

        lines.append(get_indent(indent_level) + "}")
        return "\n".join(lines)


    elif isinstance(ir, IRReturn):
        return f"return {generate_c(ir.value)}"


    elif isinstance(ir, IRBinary):
        left = generate_c(ir.left)
        right = generate_c(ir.right)
        if isinstance(left, IRBinary) or isinstance(right, IRBinary):
            return f"({left} {ir.operator} {right})"
        else:
            return f"{left} {ir.operator} {right}"
    
    elif isinstance(ir, IRUnary):
        right = generate_c(ir.operand)
        pos = ""
        if ir.postfix == False: pos = f"{ir.operator}{right}"
        else: pos = f"{right}{ir.operator}"
        if isinstance(right, IRBinary) or isinstance(right, IRUnary):
            return f"({pos})"
        else:
            return f"{pos}"

    elif isinstance(ir, IRAssignment):
        target = ir.assignee
        val = generate_c(ir.value)
        return f"{target} {ir.operator} {val}"

    elif isinstance(ir, IRCall):
        func_name = generate_c(ir.caller)

        # Remap function name if it's in aliases
        if func_name in CALL_ALIASES:
            func_name = CALL_ALIASES[func_name]

        arg_list = [generate_c(arg) for arg in ir.args]
        return f"{func_name}({', '.join(arg_list)})"

    elif isinstance(ir, IRMember):
        obj = generate_c(ir.object)
        prop = generate_c(ir.property)
        if ir.computed:
            return f"{obj}[{prop}]"
        else:
            return f"{obj}.{prop}"


    elif isinstance(ir, IRProperty):
        return f"{convert_type(ir.declared_type)} {ir.name}"


    else:
        raise NotImplementedError(f"Unhandled IR node: {type(ir).__name__}")

def get_indent(level):
    return "\t" * level

def indent_lines(lines, level):
    indent = get_indent(level)
    return [indent + line for line in lines]

def convert_type(type_: str):
    match type_:

        case "str":
            return "char*"

        case _:
            return type_

"""
IRProgram([
    IRWhile(IRBinary('<', IRIdent(a), IRConst(10)), 
    do([
        IRUnary(IRIdent(a)++)
    ])), 
    
    IRFor(
        IRVarDecl('i', int, IRConst(0)),
        IRBinary('<', IRIdent(i), IRConst(10)),
        IRUnary(IRIdent(i)++),
        do([
            IRCall(IRIdent(print), args([IRIdent(i)]))]))
        ])
"""