// expressions.go
package ast

import (
	"Gb-Script/src/lexer"
)

// Literal expressions
type NumberExpr struct {
	Value float64
}

func (n NumberExpr) expr() {}


type StringExpr struct {
	Value string
}

func (n StringExpr) expr() {}


type SymbolExpr struct {
	Value string
}

func (n SymbolExpr) expr() {}


// Complex expression
type BinaryExpr struct {
	Left Expr
	Operator lexer.Token
	Right Expr
}

func (n BinaryExpr) expr() {}