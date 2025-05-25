// types.go(ast)
package ast

type SymbolType struct {
	Name string
}

func (t SymbolType) _type() {}

type GroupType struct {
	Underlying Type
}

func (t GroupType) _type() {}
