// types.go(pasrer)
package parser

import (
	"Gb-Script/src/ast"
	"Gb-Script/src/lexer"
	"fmt"
)

type type_nud_handler func(p *parser) ast.Type
type type_led_handler func(p *parser, left ast.Type, bp binding_power) ast.Type

type type_nud_lookup map[lexer.TokenKind]type_nud_handler
type type_led_lookup map[lexer.TokenKind]type_led_handler
type type_bp_lookup map[lexer.TokenKind]binding_power

var type_bp_lu = type_bp_lookup{}
var type_nud_lu = type_nud_lookup{}
var type_led_lu = type_led_lookup{}

// Helper methods
func type_led(kind lexer.TokenKind, bp binding_power, led_fn type_led_handler) {
	type_bp_lu[kind] = bp
	type_led_lu[kind] = led_fn
}

func type_nud(kind lexer.TokenKind, nud_fn type_nud_handler) {
	type_nud_lu[kind] = nud_fn
}

func makeTokenTypeLookups() {
	type_nud(lexer.IDENT, parse_symbol_type)
	type_nud(lexer.GRP, parse_group_type)
}

func parse_type(p *parser, bp binding_power) ast.Type {
	tokKind := p.curKind()
	nud_fn, exsists := type_nud_lu[tokKind]

	if !exsists {
		// NOTE: add line number errors here
		panic(fmt.Sprintf("Type_Nud Handler expected for token %s\n", lexer.TokenKindString(tokKind)))
	}

	left := nud_fn(p)

	for type_bp_lu[p.curKind()] > bp {
		tokKind = p.curKind()
		led_fn, exsists := type_led_lu[tokKind]

		if !exsists {
			// NOTE: add line number errors here
			panic(fmt.Sprintf("Type_Led Handler expected for token %s\n", lexer.TokenKindString(tokKind)))
		}

		left = led_fn(p, left, bp_lu[p.curKind()])
	}

	return left
}

func parse_symbol_type(p *parser) ast.Type {
	return ast.SymbolType{
		Name: p.expect(lexer.IDENT).Value,
	}
}

func parse_group_type(p *parser) ast.Type {
	p.adv() // consume `GRP`
	p.expect(lexer.LESS)
	underlying_type := parse_type(p, default_bp)
	p.expect(lexer.COMMA)
	size_expr := parse_expr(p, default_bp)
	p.expect(lexer.GREATER) // <- you should also expect the closing `>`!

	numberExpr, ok := size_expr.(ast.NumberExpr)
	if !ok {
		panic("Expected a numeric literal for group size")
	}

	return ast.GroupType{
		Size:       int(numberExpr.Value),
		Underlying: underlying_type,
	}
}
