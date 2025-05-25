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

	expression := parse_expr(p, default_bp)
	p.expect(lexer.SEMICOLON)

	return ast.ExpressionStmt{
		Expression: expression,
	}
}

func parse_var_decl_stmt(p *parser) ast.Stmt {
	var explicit_type ast.Type
	var assignedVal ast.Expr

	isConst := p.adv().Kind == lexer.CONST
	varName := p.expectError(lexer.IDENT, "Inside varable declaration expected to find variable name").Value


	if p.curKind() == lexer.COLON {
		p.adv()
		explicit_type = parse_type(p, default_bp)
	}

	if p.curKind() != lexer.SEMICOLON {
		p.expect(lexer.ASSIGN)
		assignedVal = parse_expr(p, assignment)
	} else if explicit_type == nil {
		panic("Missing either right hand side in var delaration or explicit type")
	}


	p.expect(lexer.SEMICOLON)
	if isConst && assignedVal == nil {
		panic("Constant Variables must be defined")
	}

	return ast.VarDeclStmt{
		IsConst : isConst,
		Name : varName,
		AssignedVal : assignedVal,
		ExplicitType : explicit_type,
	}
}


