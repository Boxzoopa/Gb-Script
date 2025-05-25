//main.go
package main

import (
    "os"
    "Gb-Script/src/lexer"
)

func main() {
    bytes, _ := os.ReadFile("./examples/hello.gbscript") 
    src := string(bytes)
    
    tokens := lexer.Tokenize(src)

    for _, token := range tokens {
        token.Debug()
    }
}