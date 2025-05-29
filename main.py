# main.py
import sys, os
from src.lexer import Lexer
from src.parser import Parser
from src.transformer import ast_to_ir
from src.transpiler import generate_c
import json


def open_file(input_file):
    try:
        with open(input_file, 'r') as f:
            return f.read()
    except Exception as e:
        print("Failed to open file:", e)
        sys.exit(1)

def debug_lexer(toks, output=False):
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
def debug_transformer(AST, pretty=False, output=False):
    if pretty:
        ir = ast_to_ir(AST).pretty()
    else:
        ir = ast_to_ir(AST)

    if output:
        print(ir)
    
    return ir

if __name__ == "__main__":
    src = open_file("examples/08.gbscript")

    lexer = Lexer()
    tokens = lexer.tokenize(src)
    debug_lexer(tokens, output=False)

    parser = Parser(tokens)
    program = parser.parse()
    debug_parser(program, output=False)
    
    ir = debug_transformer(program, False, True)

    c_code = generate_c(ir)
    print(c_code)
    
