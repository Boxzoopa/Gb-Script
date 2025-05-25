// stmt.go
package parser

import (
	"Gb-Script/src/lexer"
	"Gb-Script/src/ast"
)

func parse_stmt (p *parser) ast.Stmt {
	stmt_fn, exsists := stmt_lu[p.curKind()]

	if exsists {
		return stmt_fn(p)
	}

	expression := parse_expr(p, defalt_bp)
	p.expect(lexer.SEMICOLON)


	return ast.ExpressionStmt {
		Expression: expression,
	}
}