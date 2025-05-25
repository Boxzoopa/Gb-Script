// parser.go
package parser

import (
	"Gb-Script/src/ast"
	"Gb-Script/src/lexer"
	"fmt"
)

type parser struct {
	tokens []lexer.Token
	pos    int
	// NOTE: Add an error array/list/slice
}

func Parse(tokens []lexer.Token) ast.BlockStmt {
	Body := make([]ast.Stmt, 0)
	p := newParser(tokens)

	for p.hasToks() {
		Body = append(Body, parse_stmt(p))
	}

	return ast.BlockStmt{
		Body: Body,
	}
}

func newParser(tokens []lexer.Token) *parser {
	makeTokenLookups()
	makeTokenTypeLookups()
	return &parser{
		tokens: tokens, pos: 0,
	}
}

// Helper Methods
func (p *parser) cur() lexer.Token {
	return p.tokens[p.pos]
}

func (p *parser) curKind() lexer.TokenKind {
	return p.cur().Kind
}

func (p *parser) adv() lexer.Token {
	tk := p.cur()
	p.pos++
	return tk
}

func (p *parser) hasToks() bool {
	return p.pos < len(p.tokens) && p.curKind() != lexer.EOF
}

func (p *parser) expectError(expectedKind lexer.TokenKind, err any) lexer.Token {
	token := p.curKind()
	kind := token

	if kind != expectedKind {
		if err == nil {
			err = fmt.Sprintf("Expected %s but recieved %s instead\n", lexer.TokenKindString(expectedKind), lexer.TokenKindString(kind))
		}

		panic(err)
	}

	return p.adv()
}

func (p *parser) expect(expectedKind lexer.TokenKind) lexer.Token {
	return p.expectError(expectedKind, nil)
}
