// statements.go
package ast

type BlockStmt struct {
	Body []Stmt
}

func (n BlockStmt) stmt() {}

type ExpressionStmt struct {
	Expression Expr
}

func (n ExpressionStmt) stmt() {}

type VarDeclStmt struct {
	Name        string
	IsConst     bool
	AssignedVal Expr
	// NOTE: Add ExplicitType
}

func (n VarDeclStmt) stmt() {}

type GrpDeclStmt struct {
	Name         string
	AssignedVals Expr//[]
	// NOTE: Add ExplicitType
}

func (n GrpDeclStmt) stmt() {}
