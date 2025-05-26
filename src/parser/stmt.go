// stmt.go
package parser

import (
	"Gb-Script/src/ast"
	"Gb-Script/src/lexer"
	"fmt"
)

func parse_stmt(p *parser) ast.Stmt {
	stmt_fn, exsists := stmt_lu[p.curKind()]
	tokKind := p.curKind()

	if exsists {
		panic(fmt.Sprintf("Unexpected token %s at start of expression. Likely parser bug.", lexer.TokenKindString(tokKind)))

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
		IsConst:      isConst,
		Name:         varName,
		AssignedVal:  assignedVal,
		ExplicitType: explicit_type,
	}
}

func parse_obj_decl_stmt(p *parser) ast.Stmt {
	p.expect(lexer.OBJ)
	var props []ast.ObjectProperty
	objName := p.expect(lexer.IDENT).Value

	p.expect(lexer.L_CURLY)

	for p.hasToks() && p.curKind() != lexer.R_CURLY {
		if p.curKind() == lexer.IDENT {
			propName := p.expect(lexer.IDENT).Value
			p.expectError(lexer.COLON, "Value Type must be explicitly declared inside object")
			objType := parse_type(p, default_bp)
			p.expect(lexer.SEMICOLON)

			// Check for duplicate properties
			for _, prop := range props {
				if prop.Property == propName {
					panic(fmt.Sprintf("Property '%s' previously defined", propName))
				}
			}

			props = append(props, ast.ObjectProperty{
				Property: propName,
				Type:     objType,
			})
			continue
		}

		// TODO: handle methods later
		panic("Cannot handle methods yet in object declaration")
	}

	p.expect(lexer.R_CURLY)

	return ast.ObjDeclStmt{
		Name:       objName,
		Properties: props,
	}
}
