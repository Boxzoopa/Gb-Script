# parser.py
from src.lexer import Lexer
from src.tokens import TokenType, Token
from src.precedence import Precedence

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

        # Pratt parsing maps
        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}
        self.register_prefix(TokenType.IDENT, self.parse_identifier)
        self.register_prefix(TokenType.NUMBER, self.parse_number)
        self.register_prefix(TokenType.LPAREN, self.parse_grouping)
        self.register_prefix(TokenType.MINUS, self.parse_prefix)
        self.register_prefix(TokenType.NOT, self.parse_prefix)

        self.register_infix(TokenType.PLUS, self.parse_infix)
        self.register_infix(TokenType.MINUS, self.parse_infix)
        self.register_infix(TokenType.MULT, self.parse_infix)
        self.register_infix(TokenType.DIV, self.parse_infix)
        self.register_infix(TokenType.EQUALS, self.parse_infix)
        self.register_infix(TokenType.NOT_EQ, self.parse_infix)

    def current(self) -> Token:
        if self.pos >= len(self.tokens):
            return Token(TokenType.EOF, "")
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.current()
        self.pos += 1
        return tok

    def match(self, kind: TokenType) -> bool:
        if self.current().kind == kind:
            self.advance()
            return True
        return False

    def parse_expression(self, precedence=Precedence.LOWEST):
        token = self.advance()
        prefix_fn = self.prefix_parse_fns.get(token.kind)
        if not prefix_fn:
            raise Exception(f"No prefix parser for token {token.kind}")
        left = prefix_fn(token)

        while (not self.at_end() and
               precedence < self.get_precedence(self.current())):
            infix_fn = self.infix_parse_fns.get(self.current().kind)
            if not infix_fn:
                break
            token = self.advance()
            left = infix_fn(left, token)

        return left

    def at_end(self):
        return self.current().kind == TokenType.EOF

    ### Pratt Registration
    def register_prefix(self, kind, fn):
        self.prefix_parse_fns[kind] = fn

    def register_infix(self, kind, fn):
        self.infix_parse_fns[kind] = fn

    ### Parse Functions
    def parse_number(self, token):
        return {"type": "number", "value": token.value}

    def parse_identifier(self, token):
        return {"type": "identifier", "name": token.value}

    def parse_grouping(self, token):
        expr = self.parse_expression()
        if not self.match(TokenType.RPAREN):
            raise Exception("Expected ')'")
        return expr

    def parse_prefix(self, token):
        right = self.parse_expression(Precedence.PREFIX)
        return {"type": "prefix", "operator": token.kind, "right": right}

    def parse_infix(self, left, token):
        precedence = self.get_precedence(token)
        right = self.parse_expression(precedence)
        return {
            "type": "binary",
            "operator": token.kind,
            "left": left,
            "right": right
        }

    def get_precedence(self, token: Token):
        if token.kind in (TokenType.PLUS, TokenType.MINUS):
            return Precedence.TERM
        elif token.kind in (TokenType.MULT, TokenType.DIV):
            return Precedence.FACTOR
        elif token.kind in (TokenType.EQUALS, TokenType.NOT_EQ):
            return Precedence.EQUALITY
        return Precedence.LOWEST
