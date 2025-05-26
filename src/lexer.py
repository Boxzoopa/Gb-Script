# lexer.py
import re
from typing import Callable
from src.tokens import Token, TokenKind

TokenHandler = Callable[[object, re.Match], None]


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.tokens = []
        self.errors = []
        self.patterns: list[tuple[re.Pattern, TokenHandler]] = []

        self._init_patterns()

    def advance(self, n: int):
        self.pos += n

    def add(self, kind: str, value: str):
        self.tokens.append(Token(kind, value))

    def remainder(self):
        return self.source[self.pos:]

    def at_eof(self):
        return self.pos >= len(self.source)

    def tokenize(self):
        while not self.at_eof():
            matched = False

            for pattern, handler in self.patterns:
                match = pattern.match(self.remainder())
                if match:
                    handler(self, match)
                    matched = True
                    break

            if not matched:
                snippet = self.remainder()[:20].replace('\n', '\\n')
                self.errors.append(f"unrecognized token near '{snippet}'")

        self.add(TokenKind.EOF, "EOF")
        return self.tokens
    def _init_patterns(self):
        self.patterns = [
            (re.compile(r'\s+'), skip_handler),
            (re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'), symbol_handler),
            (re.compile(r'//.*'), comment_handler),
            (re.compile(r'[0-9]+(?:\.[0-9]+)?'), number_handler),
            (re.compile(r'"[^"]*"'), string_handler),
            (re.compile(r"'[^']*'"), string_handler),

            # Symbols
            (re.compile(r'\('), default_handler(TokenKind.LPAREN, "(")),
            (re.compile(r'\)'), default_handler(TokenKind.RPAREN, ")")),
            (re.compile(r'\{'), default_handler(TokenKind.LCURL, "{")),
            (re.compile(r'\}'), default_handler(TokenKind.RCURL, "}")),
            (re.compile(r'\['), default_handler(TokenKind.LBRAC, "[")),
            (re.compile(r'\]'), default_handler(TokenKind.RBRAC, "]")),

            # Operators and punctuation
            (re.compile(r'=='), default_handler(TokenKind.EQUALS, "==")),
            (re.compile(r'!='), default_handler(TokenKind.NOT_EQ, "!=")),
            (re.compile(r'='), default_handler(TokenKind.ASSIGNMENT, "=")),
            (re.compile(r'!'), default_handler(TokenKind.NOT, "!")),
            (re.compile(r'<='), default_handler(TokenKind.LESS_EQ, "<=")),
            (re.compile(r'<'), default_handler(TokenKind.LESS, "<")),
            (re.compile(r'>='), default_handler(TokenKind.GREATER_EQ, ">=")),
            (re.compile(r'>'), default_handler(TokenKind.GREATER, ">")),
            (re.compile(r'\|\|'), default_handler(TokenKind.OR, "||")),
            (re.compile(r'&&'), default_handler(TokenKind.AND, "&&")),
            (re.compile(r';'), default_handler(TokenKind.SEMICOLON, ";")),
            (re.compile(r':'), default_handler(TokenKind.COLON, ":")),
            (re.compile(r'\?'), default_handler(TokenKind.QUESTION, "?")),
            (re.compile(r','), default_handler(TokenKind.COMMA, ",")),
            (re.compile(r"\."), default_handler(TokenKind.DOT, ".")),
            (re.compile(r'\+\+'), default_handler(TokenKind.P_PLUS, "++")),
            (re.compile(r'--'), default_handler(TokenKind.M_MINUS, "--")),
            (re.compile(r'\+='), default_handler(TokenKind.PLUS_EQ, "+=")),
            (re.compile(r'-='), default_handler(TokenKind.MINUS_EQ, "-=")),
            (re.compile(r'\+'), default_handler(TokenKind.PLUS, "+")),
            (re.compile(r'-'), default_handler(TokenKind.DASH, "-")),
            (re.compile(r'\*'), default_handler(TokenKind.STAR, "*")),
            (re.compile(r'/'), default_handler(TokenKind.SLASH, "/")),
            (re.compile(r'%'), default_handler(TokenKind.PERCENT, "%")),
        ]


# === HANDLERS ===

def default_handler(kind, value):
    def handler(lexer, match):
        lexer.add(kind, value)
        lexer.advance(len(value))
    return handler

def skip_handler(lexer, match):
    lexer.advance(len(match.group(0)))

def number_handler(lexer, match):
    value = match.group(0)
    lexer.add(TokenKind.NUMBER, value)
    lexer.advance(len(value))

def string_handler(lexer, match):
    full = match.group(0)
    value = full[1:-1]
    lexer.add(TokenKind.STRING, value)
    lexer.advance(len(full))

def symbol_handler(lexer, match):
    value = match.group(0)
    reserved = {
        "var": TokenKind.VAR, "const": TokenKind.CONST, "obj": TokenKind.OBJ,
        "grp": TokenKind.GRP, "new": TokenKind.NEW, "import": TokenKind.IMPORT,
        "from": TokenKind.FROM, "func": TokenKind.FUNC, "if": TokenKind.IF,
        "else": TokenKind.ELSE, "while": TokenKind.WHILE, "for": TokenKind.FOR,
        "in": TokenKind.IN
    }
    kind = reserved.get(value, TokenKind.IDENT)
    lexer.add(kind, value)
    lexer.advance(len(value))

def comment_handler(lexer, match):
    lexer.advance(len(match.group(0)))

