# main.py
import sys
from src.lexer import Lexer
from src.parser import Parser
from src.transpiler import IrTranspiler, CTranspiler
import json

from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int

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
def debug_transpiler(program, to: str = "ir", store: bool=False):
    match to:
        case 'ir' | 'IR' | 'Ir':
            ir_transpiler = IrTranspiler()
            ir_transpiler.transpile(program)

            module = ir_transpiler.module
            module.triple = llvm.get_default_triple()

            if store == True:
                with open("debug/ir.ll", "w") as f:
                    f.write(str(module))
            else:
                print('\nTranspiled IR Output:')
                print(str(module))

        case 'c' | 'C':        
            c_transpiler = CTranspiler()
            c_transpiler.transpile(program)

            if store == True:
                with open("output.c", "w") as f:
                    f.write('\n'.join(c_transpiler.code))
            
            else:
                print('\nTranspiled C Output:')
                print('\n'.join(c_transpiler.code))



            

if __name__ == "__main__":
    src = open_file("examples/01.gbscript")

    lexer = Lexer()
    tokens = lexer.tokenize(src)

    debug_lexer(tokens, output=False)

    parser = Parser(tokens)
    program = parser.parse()
    
    debug_parser(program, output=False)

    debug_transpiler(program, 'ir')
    debug_transpiler(program, 'c')






    

