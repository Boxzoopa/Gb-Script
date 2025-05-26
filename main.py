# main.py
import sys
from src.lexer import Lexer
from src.parser import Parser
import json

def open_file(input_file):
    try:
        with open(input_file, 'r') as f:
            source = f.read()
            return source

    except Exception as e:
        print("Failed to open file: ", e)
        sys.exit(1)


if __name__ == "__main__":
    src = open_file("examples/01.gbscript")

    lexer = Lexer(src)
    tokens = lexer.tokenize()
    if lexer.errors :
        print("Lexer errors:")
        for err in lexer.errors:
            print(" -", err)
        exit(1)
    #for tok in tokens:
    #    print(tok)

    parser = Parser(tokens)
    program = parser.parse()

    if parser.errors :
        print("Parser errors:")
        for err in parser.errors:
            print(" -", err)
        exit(1)

    json_output = json.dumps(program.to_dict(), indent=2)
    print(json_output)

    

