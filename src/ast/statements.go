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
	Name         string
	IsConst      bool
	AssignedVal  Expr
	ExplicitType Type
}

func (n VarDeclStmt) stmt() {}

type MethodStmt struct {
	// Note: add type i.e func<int> function() {}
	
	
}

type ObjectProperty struct {
	// MAYBE: add bool IsStatic
	Property string
	Type Type
}

type ObjDeclStmt struct {
	Name string
	Properties []ObjectProperty
}

func (n ObjDeclStmt) stmt() {}