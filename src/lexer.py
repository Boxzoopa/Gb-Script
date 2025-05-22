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

    def tokenize(self):
        while not self.at_end():
            self.start = self.pos
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, ""))
        return self.tokens

    ## UTILS FUNCTIONS
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
    
    def match(self, expected):
        if self.at_end(): return False
        if self.source[self.pos] != expected: return False
        self.pos += 1
        return True

    
    ## TOKENIZING
    def scan_token(self):
        c = self.advance()

        if c.isspace():
            return
        
        if c in ("'", '"'):
            self.lex_string(c)
            return
        
        if c.isdigit():
            self.lex_number()
            return

        if c.isalpha():
            self.lex_identifier()
            return
        
        elif c == '+':
            if self.match('+'):
                self.tokens.append(Token(TokenType.P_PLUS, '++'))
            elif self.match('='):
                self.tokens.append(Token(TokenType.P_EQ, '+='))
            else:
                self.tokens.append(Token(TokenType.PLUS, '+'))

        elif c == '-':
            if self.match('-'):
                self.tokens.append(Token(TokenType.M_MINUS, '--'))
            elif self.match('='):
                self.tokens.append(Token(TokenType.M_EQ, '-='))
            else:
                self.tokens.append(Token(TokenType.MINUS, '-'))

        elif c in ("'", '"'):
            self.lex_string(c)

        elif c == "*":
            self.tokens.append(Token(TokenType.MULT, "*"))
        elif c == "/":
            self.tokens.append(Token(TokenType.DIV, "/"))
        elif c == "^":
            self.tokens.append(Token(TokenType.POW, "/"))

        elif c == "=":
            if self.match("="):
                self.tokens.append(Token(TokenType.EQUALS, "=="))
            else:
                self.tokens.append(Token(TokenType.ASSIGN, "="))

        elif c == '!':
            if self.match('='):
                self.tokens.append(Token(TokenType.NOT_EQ, '!='))
            else:
                self.tokens.append(Token(TokenType.NOT, '!'))

        elif c == ";":
            self.tokens.append(Token(TokenType.SEMICOLON, ";"))
        elif c == ':':
            self.tokens.append(Token(TokenType.COLON, ':'))
        elif c == "?":
            self.tokens.append(Token(TokenType.QUESTION, '?'))
        elif c == ",":
            self.tokens.append(Token(TokenType.COMMA, ','))

        elif c == '(':
            self.tokens.append(Token(TokenType.LPAREN, '('))
        elif c == ')':
            self.tokens.append(Token(TokenType.RPAREN, ')'))
        elif c == '{':
            self.tokens.append(Token(TokenType.LCURL, '{'))
        elif c == '}':
            self.tokens.append(Token(TokenType.RCURL, '}'))
        elif c == '[':
            self.tokens.append(Token(TokenType.LBRAC, '['))
        elif c == ']':
            self.tokens.append(Token(TokenType.RBRAC, ']'))
        
        
        

        else:
            raise Exception(f"Unexpected character: '{c}'")
            
    def lex_number(self):
        start = self.pos - 1
        while self.peek().isdigit():
            self.advance()
        value = self.source[start:self.pos]
        self.tokens.append(Token(TokenType.NUMBER, value))

    def lex_identifier(self):
        start = self.pos - 1
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[start:self.pos]
        token_type = keywords.get(text, TokenType.IDENT)
        self.tokens.append(Token(token_type, text))    
    
    def lex_string(self, quote_type: str):
        start = self.pos
        while not self.at_end() and self.peek() != quote_type:
            self.advance()
        if self.at_end():
            raise Exception("Unterminated string literal.")
        self.advance()  # Consume closing "
        value = self.source[start:self.pos - 1]
        self.tokens.append(Token(TokenType.STRING, value))