# main.py
import sys
from src.lexer import Lexer
from src.p_parser import Parser

def run_file(input_file, output_file=None):
    try:
        with open(input_file, 'r') as f:
            source = f.read()

        lexer = Lexer(source)
        toks = lexer.tokenize()
        for tok in toks: 
            print(tok)
        parser = Parser(toks, source)
        ast = parser.parse()
        print(ast)

    except Exception as e:
        print("Failed to run:", e)


if __name__ == "__main__":
    run_file("examples/groups.gbscript")