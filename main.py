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
def debug_lexer(toks, output =False):
    if lexer.errors:
        print("GBSCRIPT::Lexer errors:")
        for err in lexer.errors:
            print(" -", err)
        exit(1)

    if output:
        for tok in toks:
            print(tok)
def debug_parser(program, output=False):
    if parser.errors:
        print("GBSCRIPT::Parser errors:")
        for err in parser.errors:
            print(" -", err)
        exit(1)

    if output:
        print(json.dumps(program.to_dict(), indent=3))

if __name__ == "__main__":
    src = open_file("examples/05.gbscript")

    lexer = Lexer()
    tokens = lexer.tokenize(src)

    debug_lexer(tokens, output=True)

    parser = Parser(tokens)
    program = parser.parse()
    
    debug_parser(program, output=True)

    

