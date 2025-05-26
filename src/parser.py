from src.nodes import *
from src.tokens import Token, TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = []


    def not_at_end(self):
        return self.tokens[0].type != TokenType.EOF
    
    def at(self): # get current token
        return self.tokens[0]

    def adv(self): # consume current token
        prev = self.tokens.pop(0)
        return prev
    
    def expect(self, expected_type):
        if self.at().type == expected_type:
            return self.adv()
        else:
            self.errors.append(f"Expected token {expected_type} at line {self.at().ln}, col {self.at().col}, but found {self.at().value}")
            return None


    def parse(self):
        body = []

        while self.not_at_end():
            stmt = self.parse_stmt()
            if stmt:
                body.append(stmt)


        return Program(body)
    
    def parse_stmt(self):
        # TODO: Force Semicolon at the end of each statement
        expr = self.parse_expr()

        if self.at().type == TokenType.SEMICOLON:
            self.adv()
        else:
            self.errors.append(f"Expected ';' at line {self.at().ln}, col {self.at().col}, but found {self.at().value}")
            
        return expr
    
    def parse_expr(self):
        return self.parse_additive()
    

    def parse_additive(self):
        left = self.parse_multiplicitave()

        while self.at().type in (TokenType.PLUS, TokenType.DASH):
            op = self.adv().value
            right = self.parse_multiplicitave()
            left = BinaryExpr(left, right, op)

        return left
    def parse_multiplicitave(self):
        left = self.parse_primary()

        while self.at().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.adv().value
            right = self.parse_primary()
            left = BinaryExpr(left, right, op)

        return left

    def parse_primary(self):
        tk = self.at().type

        match tk:
            case TokenType.IDENT:
                return Identifier(self.adv().value)
            case TokenType.NUMBER:
                return NumericLiteral(int(self.adv().value))
            case TokenType.LPAREN:
                self.adv() # consume '('
                value = self.parse_expr()
                self.expect(TokenType.RPAREN) # consume ')'
                return value
            
            case default:
                self.errors.append(f"Unexpected token {self.at().value} at {self.at().ln}, {self.at().col}")
                self.adv()
                return None

