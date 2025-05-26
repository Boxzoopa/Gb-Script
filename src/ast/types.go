// types.go(ast)
package ast

type SymbolType struct {
	Name string
}

func (t SymbolType) _type() {}

type GroupType struct {
	Underlying Type
	Size       int
}

func (t GroupType) _type() {}
