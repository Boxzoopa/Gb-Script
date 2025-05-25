// expr.go
package parser

import (
	"Gb-Script/src/ast"
	"Gb-Script/src/lexer"
	"fmt"
	"strconv"
)

func parse_expr(p *parser, bp binding_power) ast.Expr {
	tokKind := p.curKind()
	nud_fn, exsists := nud_lu[tokKind]

	if !exsists {
		// NOTE: add line number errors here
		panic(fmt.Sprintf("Nud Handler expected for token %s\n", lexer.TokenKindString(tokKind)))
	}

	left := nud_fn(p)

	for bp_lu[p.curKind()] > bp {
		tokKind = p.curKind()
		led_fn, exsists := led_lu[tokKind]

		if !exsists {
			// NOTE: add line number errors here
			panic(fmt.Sprintf("Led Handler expected for token %s\n", lexer.TokenKindString(tokKind)))
		}

		left = led_fn(p, left, bp)
	}

	return left
}

func parse_primary_expr(p *parser) ast.Expr {
	switch p.curKind() {
	case lexer.NUMBER:
		number, _ := strconv.ParseFloat(p.adv().Value, 64)
		return ast.NumberExpr{
			Value: number,
		}
	case lexer.STRING:
		return ast.StringExpr{
			Value: p.adv().Value,
		}
	case lexer.IDENT:
		return ast.SymbolExpr{
			Value: p.adv().Value,
		}
	default:
		panic(fmt.Sprintf("Cannot create primary expression from %s\n", lexer.TokenKindString(p.curKind())))

	}

	return nil

}

func parse_binary_expr(p *parser, left ast.Expr, bp binding_power) ast.Expr {
	opToken := p.adv()
	right := parse_expr(p, bp)

	return ast.BinaryExpr{
		Left:     left,
		Operator: opToken,
		Right:    right,
	}
}
