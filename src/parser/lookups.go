// lookups.go
package parser

import (
	"Gb-Script/src/ast"
	"Gb-Script/src/lexer"
)

type binding_power int

const (
	default_bp binding_power = iota
	comma
	assignment
	logical
	relational
	additive
	multiplicative
	unary
	call
	member
	primary
)

type stmt_handler func(p *parser) ast.Stmt
type nud_handler func(p *parser) ast.Expr
type led_handler func(p *parser, left ast.Expr, bp binding_power) ast.Expr

type stmt_lookup map[lexer.TokenKind]stmt_handler
type nud_lookup map[lexer.TokenKind]nud_handler
type led_lookup map[lexer.TokenKind]led_handler
type bp_lookup map[lexer.TokenKind]binding_power

var bp_lu = bp_lookup{}
var nud_lu = nud_lookup{}
var led_lu = led_lookup{}
var stmt_lu = stmt_lookup{}

// Helper methods
func led(kind lexer.TokenKind, bp binding_power, led_fn led_handler) {
	bp_lu[kind] = bp
	led_lu[kind] = led_fn
}

func nud(kind lexer.TokenKind, nud_fn nud_handler) {
	nud_lu[kind] = nud_fn
}

func stmt(kind lexer.TokenKind, stmt_fn stmt_handler) {
	bp_lu[kind] = default_bp
	stmt_lu[kind] = stmt_fn
}

func makeTokenLookups() {
	led(lexer.ASSIGN, assignment, parse_assignment_expr)
	led(lexer.PLUS_EQ, assignment, parse_assignment_expr)
	led(lexer.DASH_EQ, assignment, parse_assignment_expr)
	// NOTE: add *= /=

	// Logical
	led(lexer.AND, logical, parse_binary_expr)
	led(lexer.OR, logical, parse_binary_expr)
	led(lexer.DOT_DOT, logical, parse_binary_expr)

	// Relational
	led(lexer.LESS, relational, parse_binary_expr)
	led(lexer.LESS_EQ, relational, parse_binary_expr)
	led(lexer.GREATER, relational, parse_binary_expr)
	led(lexer.GREATER_EQ, relational, parse_binary_expr)
	led(lexer.ASSIGN, relational, parse_binary_expr)
	led(lexer.NOT_EQ, relational, parse_binary_expr)

	// Additive & Multiplicative
	led(lexer.PLUS, additive, parse_binary_expr)
	led(lexer.DASH, additive, parse_binary_expr)

	led(lexer.STAR, multiplicative, parse_binary_expr)
	led(lexer.SLASH, multiplicative, parse_binary_expr)
	led(lexer.PERCENT, multiplicative, parse_binary_expr)

	// Literals & sybmols
	nud(lexer.NUMBER, parse_primary_expr)
	nud(lexer.STRING, parse_primary_expr)
	nud(lexer.IDENT, parse_primary_expr)
	nud(lexer.L_PAREN, parse_grouping_expr)
	nud(lexer.DASH, parse_unary_expr)

	// Call/Member
	led(lexer.L_PAREN, call, parse_obj_init_expr)
	nud(lexer.L_BRACK, parse_group_init_expr)

	// Statements
	stmt(lexer.CONST, parse_var_decl_stmt)
	stmt(lexer.VAR, parse_var_decl_stmt)
	stmt(lexer.OBJ, parse_obj_decl_stmt)
}
