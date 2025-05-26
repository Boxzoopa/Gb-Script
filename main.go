// main.go
package main

import (
	"Gb-Script/src/lexer"
	"Gb-Script/src/parser"
	"fmt"
	"os"

	"github.com/sanity-io/litter"
)

var DebugL bool = false
var DebugP bool = true

func main() {
	bytes, _ := os.ReadFile("./examples/04.gbscript")
	src := string(bytes)

	tokens := lexer.Tokenize(src)

	if DebugL == true {
		fmt.Printf("Tokens: \n")
		for _, token := range tokens {
			token.Debug()
		}
	}

	if DebugP == true {
		fmt.Printf("AST: \n")
		ast := parser.Parse(tokens)
		litter.Dump(ast)
	}
}
