# lexer.py
from src.tokens import TokenType, Token

keywords = {
    "var": TokenType.VAR,
    "const": TokenType.CONST,
    "func": TokenType.FUNC,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "from": TokenType.FROM,
    "import": TokenType.IMPORT,
    "or": TokenType.OR,
    "in": TokenType.IN,
    "new": TokenType.NEW,
    "grp": TokenType.GRP,
    "obj": TokenType.OBJECT,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "str": TokenType.STR,
    "bool": TokenType.BOOL,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.pos = 0
        self.tokens = []
        self.line = 1

    def tokenize(self):
        while not self.at_end():
            self.start = self.pos
            self.scan_token()
        self.add_token(TokenType.EOF)
        return self.tokens

    ## UTILITIES

    def at_end(self):
        return self.pos >= self.length

    def advance(self):
        char = self.source[self.pos]
        self.pos += 1
        return char

    def peek(self):
        if self.at_end():
            return '\0'
        return self.source[self.pos]

    def peek_next(self):
        if self.pos + 1 >= self.length:
            return '\0'
        return self.source[self.pos + 1]

    def match(self, expected):
        if self.at_end():
            return False
        if self.source[self.pos] != expected:
            return False
        self.pos += 1
        return True

    def add_token(self, kind: TokenType, value: str = None):
        lexeme = self.source[self.start:self.pos] if value is None else value
        self.tokens.append(Token(kind, lexeme, self.line))

    ## TOKENIZER

    def scan_token(self):
        c = self.advance()

        if c in ' \r\t':
            return
        if c == '\n':
            self.line += 1
            return

        if c in ("'", '"'):
            self.lex_string(c)
            return

        if c.isdigit():
            self.lex_number()
            return

        if c.isalpha() or c == "_":
            self.lex_identifier()
            return


        # Single or multi-character operators
        match c:
            case '+':
                if self.match('+'):
                    self.add_token(TokenType.P_PLUS)
                elif self.match('='):
                    self.add_token(TokenType.P_EQ)
                else:
                    self.add_token(TokenType.PLUS)

            case '-':
                if self.match('-'):
                    self.add_token(TokenType.M_MINUS)
                elif self.match('='):
                    self.add_token(TokenType.M_EQ)
                else:
                    self.add_token(TokenType.MINUS)

            case '*':
                self.add_token(TokenType.MULT)

            case '/':
                if self.match('/'):
                    self.lex_comment()
                    return
                else:
                    self.add_token(TokenType.DIV)
                    return


            case '^':
                self.add_token(TokenType.POW)

            case '=':
                if self.match('='):
                    self.add_token(TokenType.EQUALS)
                else:
                    self.add_token(TokenType.ASSIGN)

            case '!':
                if self.match('='):
                    self.add_token(TokenType.NOT_EQ)
                else:
                    self.add_token(TokenType.NOT)

            case ';': self.add_token(TokenType.SEMICOLON)
            case ':': self.add_token(TokenType.COLON)
            case '?': self.add_token(TokenType.QUESTION)
            case ',': self.add_token(TokenType.COMMA)
            case '(': self.add_token(TokenType.LPAREN)
            case ')': self.add_token(TokenType.RPAREN)
            case '{': self.add_token(TokenType.LCURL)
            case '}': self.add_token(TokenType.RCURL)
            case '[': self.add_token(TokenType.LBRAC)
            case ']': self.add_token(TokenType.RBRAC)

            case _:
                raise Exception(f"[Line {self.line}] Unexpected character: '{c}'")

    def lex_number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()  # consume '.'
            while self.peek().isdigit():
                self.advance()
        value = self.source[self.start:self.pos]
        self.add_token(TokenType.NUMBER, value)

    def lex_identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start:self.pos]
        token_type = keywords.get(text, TokenType.IDENT)
        self.add_token(token_type, text)

    def lex_string(self, quote_type: str):
        while not self.at_end() and self.peek() != quote_type:
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.at_end():
            raise Exception(f"[Line {self.line}] Unterminated string literal.")
        self.advance()  # consume closing quote
        value = self.source[self.start + 1:self.pos - 1]
        self.add_token(TokenType.STRING, value)



    def lex_comment(self):
        self.advance()  # consume first '/'
        self.advance()  # consume second '/'
        while not self.at_end() and self.peek() != '\n':
            self.advance()
        return

