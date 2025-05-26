from src.nodes import *
from src.tokens import Token, TokenKind
from enum import IntEnum, auto
from typing import Callable, Dict

# ----------------------------
# Binding Power Precedence
# ----------------------------
class BindingPower(IntEnum):
    DEFAULT_BP = 0
    COMMA = auto()
    ASSIGNMENT = auto()
    LOGICAL = auto()
    RELATIONAL = auto()
    ADDITIVE = auto()
    MULTIPLICATIVE = auto()
    UNARY = auto()
    CALL = auto()
    MEMBER = auto()
    PRIMARY = auto()

# ----------------------------
# NUD / LED Registries
# ----------------------------
nud_table: Dict[TokenKind, Callable] = {}
led_table: Dict[TokenKind, tuple[int, Callable]] = {}

def nud(kind: TokenKind, func: Callable):
    nud_table[kind] = func

def led(kind: TokenKind, bp: int, func: Callable):
    led_table[kind] = (bp, func)

# ----------------------------
# Parser Class
# ----------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.create_lookups()

    def current(self):
        if self.pos >= len(self.tokens):
            return Token(TokenKind.EOF, None)
        return self.tokens[self.pos]

    def advance(self):
        tok = self.current()
        if self.pos < len(self.tokens):
            self.pos += 1
        return tok

    def hasTokens(self) -> bool:
        return self.pos < len(self.tokens) and self.current().kind != TokenKind.EOF

    def expect(self, kind):
        if self.current().kind != kind:
            self.errors.append(f"Expected {kind}, got {self.current().kind}")
            return False
        self.advance()
        return True

    def parse(self):
        stmts = []
        while self.hasTokens():
            # Skip semicolons between statements
            while self.current().kind == TokenKind.SEMICOLON:
                self.advance()
                if self.current().kind == TokenKind.EOF:
                    break

            if self.current().kind == TokenKind.EOF:
                break

            stmt = self.parse_stmt()
            if stmt:
                stmts.append(stmt)

        return ProgramStmt(stmts)

    def parse_stmt(self):
        tok = self.current()
        if tok.kind in nud_table:
            expr = self.parse_expr()
            self.expect(TokenKind.SEMICOLON)
            return ExpressionStmt(expr)
        else:
            self.errors.append(f"Unexpected token {tok.kind} at start of statement")
            self.advance()
            return None

    def parse_expr(self, bp=0):
        if self.current().kind == TokenKind.EOF:
            self.errors.append("Unexpected EOF while parsing expression")
            return NumberExpr(0)

        tok = self.advance()
        if tok.kind not in nud_table:
            self.errors.append(f"No nud for {tok.kind}")
            return NumberExpr(0)

        left = nud_table[tok.kind](self, tok)

        while True:
            op = self.current()
            entry = led_table.get(op.kind)
            if not entry or entry[0] <= bp:
                break
            self.advance()
            led_bp, led_fn = entry
            left = led_fn(self, left, op)

        return left

    def create_lookups(self):
        # NUD handlers (literals, identifiers)
        nud(TokenKind.NUMBER, parse_literal)
        nud(TokenKind.STRING, parse_literal)
        nud(TokenKind.IDENT, parse_literal)

        # LED handlers (infix binary ops)
        led(TokenKind.PLUS, BindingPower.ADDITIVE, parse_binary_expr)
        led(TokenKind.STAR, BindingPower.MULTIPLICATIVE, parse_binary_expr)
        led(TokenKind.EQUALS, BindingPower.RELATIONAL, parse_binary_expr)
        led(TokenKind.LESS, BindingPower.RELATIONAL, parse_binary_expr)

# ----------------------------
# Expression Parsers
# ----------------------------
def parse_literal(parser: Parser, tok: Token):
    if tok.kind == TokenKind.NUMBER:
        return NumberExpr(tok.value)
    elif tok.kind == TokenKind.STRING:
        return StringExpr(tok.value)
    elif tok.kind == TokenKind.IDENT:
        return SymbolExpr(tok.value)
    else:
        parser.errors.append(f"Unexpected token in parse_literal: {tok}")
        return NumberExpr(0)

def parse_binary_expr(parser: Parser, left: Expr, op: Token):
    bp, _ = led_table[op.kind]
    right = parser.parse_expr(bp)
    return BinaryExpr(left, right, op)
