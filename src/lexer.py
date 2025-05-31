# lexer.py
from src.tokens import Token, TokenType

KEYWORDS = {
    "var": TokenType.VAR,
    "const": TokenType.CONST,
    "obj": TokenType.OBJ,
    "grp": TokenType.GRP,
    "func": TokenType.FUNC,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "or": TokenType.OR,
    "and": TokenType.AND,
    "module": TokenType.MODULE,
    "import": TokenType.IMPORT,
    "from": TokenType.FROM,
    "null": TokenType.NULL,
    "return": TokenType.RETURN,
    "func" : TokenType.FUNC,
    "state" : TokenType.STATE,
    "spr" : TokenType.SPRITE
}

WHITESPACE = {' ', '\t'}

SINGLE_CHAR_TOKENS = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LCURL,
    "}": TokenType.RCURL,
    "[": TokenType.LBRAC,
    "]": TokenType.RBRAC,
    ";": TokenType.SEMICOLON,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "%": TokenType.PERCENT,
}

class Lexer:
    def __init__(self):
        self.tokens = []
        self.errors = []
        self.ln = 1
        self.col = 1
        self.pos = 1

    def add_token(self, kind: TokenType, value: str = ""):
        self.tokens.append(Token(kind, value, self.ln, self.col))
        self.col += len(value)

    def peek(self, source: str, i: int, offset: int = 1):
        pos = i + offset
        if pos < len(source):
            return source[pos]
        return None

    def lex_string(self, source: str, i: int):
        start_line, start_col = self.ln, self.col
        i += 1  # skip opening quote
        self.col += 1
        start = i
        length = len(source)
        while i < length and source[i] != '"':
            if source[i] == '\n':
                self.ln += 1
                self.col = 1
                i += 1
            else:
                i += 1
                self.col += 1
        val = source[start:i]
        if i < length:
            i += 1  # skip closing quote
            self.col += 1
            self.add_token(TokenType.STRING, val)
        else:
            self.errors.append(f"Unterminated string at line {start_line} col {start_col}")
        return i

    def lex_number(self, source: str, i: int):
        start = i
        length = len(source)
        while i < length and source[i].isdigit():
            i += 1
            self.col += 1
        val = source[start:i]
        self.add_token(TokenType.NUMBER, val)
        return i

    def lex_identifier(self, source: str, i: int):
        start = i
        length = len(source)
        while i < length and (source[i].isalnum() or source[i] == '_'):
            i += 1
            self.col += 1
        val = source[start:i]
        kind = KEYWORDS.get(val, TokenType.IDENT)
        self.add_token(kind, val)
        return i

    def tokenize(self, source: str):
        i = 0
        length = len(source)

        while i < length:
            ch = source[i]

            # Whitespace
            if ch in WHITESPACE:
                self.col += 1
                i += 1
                continue
            elif ch == '\n':
                self.ln += 1
                self.col = 1
                i += 1
                continue

            # Comments
            if ch == '/' and self.peek(source, i) == '/':
                i += 2
                self.col += 2
                while i < length and source[i] != '\n':
                    i += 1
                    self.col += 1
                continue

            # Single-char tokens
            if ch in SINGLE_CHAR_TOKENS:
                self.add_token(SINGLE_CHAR_TOKENS[ch], ch)
                i += 1
                continue

            # Two-char or one-char operators
            def match_two_char(op1, op2, token_two, token_one):
                if ch == op1:
                    if self.peek(source, i) == op2:
                        self.add_token(token_two, op1 + op2)
                        return 2
                    else:
                        self.add_token(token_one, op1)
                        return 1
                return 0

            # Two-char or one-char operators
            if ch == '=':
                if self.peek(source, i) == '=':
                    self.add_token(TokenType.EQUALS, '==')
                    i += 2
                    self.col += 2
                else:
                    self.add_token(TokenType.ASSIGNMENT, '=')
                    i += 1
                    self.col += 1
                continue
            elif ch == '+':
                if self.peek(source, i) == '+':
                    self.add_token(TokenType.P_PLUS, '++')
                    i += 2
                    self.col += 2
                elif self.peek(source, i) == '=':
                    self.add_token(TokenType.PLUS_EQ, '+=')
                    i += 2
                    self.col += 2
                else:
                    self.add_token(TokenType.PLUS, '+')
                    i += 1
                    self.col += 1
                continue
            elif ch == '-':
                if self.peek(source, i) == '-':
                    self.add_token(TokenType.M_MINUS, '--')
                    i += 2
                    self.col += 2
                elif self.peek(source, i) == '=':
                    self.add_token(TokenType.MINUS_EQ, '-=')
                    i += 2
                    self.col += 2
                else:
                    self.add_token(TokenType.DASH, '-')
                    i += 1
                    self.col += 1
                continue
            elif ch == '!':
                if self.peek(source, i) == '=':
                    self.add_token(TokenType.NOT_EQ, '!=')
                    i += 2
                    self.col += 2
                else:
                    self.add_token(TokenType.NOT, '!')
                    i += 1
                    self.col += 1
                continue
            elif ch == '&':
                if self.peek(source, i) == '&':
                    self.add_token(TokenType.AND, '&&')
                    i += 2
                    self.col += 2
                continue
            elif ch == '<':
                if self.peek(source, i) == '=':
                    self.add_token(TokenType.LESS_EQ, '<=')
                    i += 2
                    self.col += 2
                else:
                    self.add_token(TokenType.LESS, '<')
                    i += 1
                    self.col += 1
                continue
            elif ch == '>':
                if self.peek(source, i) == '=':
                    self.add_token(TokenType.GREATER_EQ, '>=')
                    i += 2
                    self.col += 2
                else:
                    self.add_token(TokenType.GREATER, '>')
                    i += 1
                    self.col += 1
                continue


            # String literal
            if ch == '"':
                i = self.lex_string(source, i)
                continue

            # Number literal
            if ch.isdigit():
                i = self.lex_number(source, i)
                continue

            # Identifier or keyword
            if ch.isalpha() or ch == '_':
                i = self.lex_identifier(source, i)
                continue

            # Unknown character
            self.errors.append(f"Unexpected character: '{ch}' at line {self.ln}, col {self.col}")
            i += 1
            self.col += 1

        self.add_token(TokenType.EOF, "")
        return self.tokens
