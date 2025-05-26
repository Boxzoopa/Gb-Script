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

type UnaryExpr struct {
	Operator lexer.Token
	Right Expr
}

func (n UnaryExpr) expr() {}

type AssignmentExpr struct {
	Assignee Expr
	Operator lexer.Token
	Value Expr // Right hand side
}

func (n AssignmentExpr) expr() {}


type ObjectInstantiation struct {
	ObjName string
	Parameters []Expr
}

func (n ObjectInstantiation) expr() {}

type GroupInstantiation struct {
	//Underlying Type
	Contents []Expr
}

func (n GroupInstantiation) expr() {}