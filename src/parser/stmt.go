// stmt.go
package parser

import (
	"Gb-Script/src/ast"
	"Gb-Script/src/lexer"
)

func parse_stmt(p *parser) ast.Stmt {
	stmt_fn, exsists := stmt_lu[p.curKind()]

	if exsists {
		return stmt_fn(p)
	}

	expression := parse_expr(p, defalt_bp)
	p.expect(lexer.SEMICOLON)

	return ast.ExpressionStmt{
		Expression: expression,
	}
}

func parse_var_decl_stmt(p *parser) ast.Stmt {
	isConst := p.adv().Kind == lexer.CONST
	varName := p.expectError(lexer.IDENT, "Inside varable declaration expected to find variable name").Value

	p.expect(lexer.ASSIGN)
	assignedVal := parse_expr(p, assignment)
	p.expect(lexer.SEMICOLON)

	return ast.VarDeclStmt{
		IsConst : isConst,
		Name : varName,
		AssignedVal : assignedVal,
	}
}

func parse_grp_decl_stmt(p *parser) ast.Stmt {
	p.adv()
	varName := p.expectError(lexer.IDENT, "Inside varable declaration expected to find variable name").Value

	p.expect(lexer.ASSIGN)
	assignedVal := parse_expr(p, assignment)
	p.expect(lexer.SEMICOLON)

	return ast.GrpDeclStmt{
		Name : varName,
		AssignedVals : assignedVal,
	}
}
