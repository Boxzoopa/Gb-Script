import sys
import json
import argparse
from src.lexer import Lexer
from src.parser import Parser
from src.transformer import ast_to_ir
from src.transpiler import generate_c
from src.sprite import Sprite

def open_file(input_file):
    try:
        with open(input_file, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error: Failed to open file '{input_file}': {e}")
        sys.exit(1)

def save_file(output_file, content):
    try:
        with open(output_file, 'w') as f:
            f.write(content)
        print(f"Output written to {output_file}")
    except Exception as e:
        print(f"Error: Failed to write to file '{output_file}': {e}")
        sys.exit(1)

def debug_lexer(lexer, tokens, output=False):
    if lexer.errors:
        print("GBSCRIPT Lexer errors:")
        for err in lexer.errors:
            print(" -", err)
        sys.exit(1)
    if output:
        for tok in tokens:
            print(tok)

def debug_parser(parser, program, output=False):
    if parser.errors:
        print("GBSCRIPT Parser errors:")
        for err in parser.errors:
            print(" -", err)
        sys.exit(1)
    if output:
        print(json.dumps(program.to_dict(), indent=3))

def debug_transformer(ast, pretty=False, output=False):
    ir = ast_to_ir(ast)
    if pretty:
        ir = ir.pretty()
    if output:
        print(ir)
    return ir

def run_transpile(args):
    input_f = args.input_file 

    if not args.input_file.endswith(".gbs"):
        print("Error: Input file must have a .gbs extension.")
        sys.exit(1)

    src = open_file(args.input_file)

    lexer = Lexer()
    tokens = lexer.tokenize(src)
    debug_lexer(lexer, tokens, output=args.debug_lexer)

    parser_instance = Parser(tokens, input_f)
    program = parser_instance.parse()
    debug_parser(parser_instance, program, output=args.debug_parser)

    ir = debug_transformer(program, pretty=False, output=args.debug_ir)

    c_code = generate_c(ir)

    if args.output:
        save_file(args.output, c_code)
    else:
        print(c_code)

def run_view_sprite(args):
    sprite = Sprite.from_file(args.sprite_file)
    print(f"Sprite Name: {sprite.name}")
    sprite.print_ascii()

def main():
    parser = argparse.ArgumentParser(description="GBScript Transpiler and Tools (GBSB)")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: transpile
    transpile_parser = subparsers.add_parser("build", help="Transpile a .gbs file to C")
    transpile_parser.add_argument("input_file", help="Path to .gbs source file")
    transpile_parser.add_argument("-o", "--output", help="Path to output .c file")
    transpile_parser.add_argument("--debug-lexer", action="store_true", help="Print tokens")
    transpile_parser.add_argument("--debug-parser", action="store_true", help="Print AST")
    transpile_parser.add_argument("--debug-ir", action="store_true", help="Print IR")
    transpile_parser.set_defaults(func=run_transpile)

    # Subcommand: view-sprite
    sprite_parser = subparsers.add_parser("spr", help="View a sprite from a .gbspr file")
    sprite_parser.add_argument("sprite_file", help="Path to .gbspr sprite file")
    sprite_parser.set_defaults(func=run_view_sprite)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == "__main__":
    main()