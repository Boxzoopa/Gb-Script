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
            self.errors.append(f"Expected token {expected_type} at line {self.at().ln}, col {self.at().col}, but found '{self.at().value}'")
            return None


    def parse(self):
        body = []

        while self.not_at_end():
            stmt = self.parse_stmt()
            if stmt:
                body.append(stmt)


        return Program(body)
    
    def parse_stmt(self):
        match self.at().type:
            case TokenType.VAR:
                return self.parse_var_decl()
            case TokenType.CONST:
                return self.parse_var_decl()
            
            case default:
                expr = self.parse_expr()
                self.expect(TokenType.SEMICOLON)
                return expr
    
    def parse_type(self):
        if self.at().type == TokenType.IDENT:
            type_name = self.adv().value
            print(type_name)
            if type_name not in ("int", "str", "bool", "float"):
                self.errors.append(f"Unsupported type '{type_name}' at line {self.at().ln}, col {self.at().col}")
                return None
            return type_name
        else:
            self.errors.append(f"Expected type identifier at line {self.at().ln}, col {self.at().col}")
            return None

    def parse_var_decl(self):
        is_const = self.adv().type == TokenType.CONST
        name = self.expect(TokenType.IDENT).value
        type_name = None

        # TODO: add explicit type annotation support i.e var a: int = 5;
        if self.at().type == TokenType.COLON:
            self.adv()
            type_name = self.parse_type()

        if self.at().type == TokenType.SEMICOLON:
            self.adv()
            if is_const:
                self.errors.append(f"Constant variable '{name}' must be initialized, at line {self.at().ln}, col {self.at().col}")

            return VariableDecleration(
                name, is_const=is_const, value=None, explicit_type=type_name
            )
        
        self.expect(TokenType.ASSIGNMENT)
        assigned_value = self.parse_expr()
        self.expect(TokenType.SEMICOLON)

        return VariableDecleration(
            name, is_const=is_const, value=assigned_value, explicit_type=type_name
        )

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
            
            
            case TokenType.NULL:
                self.adv()
                return NullLiteral()
            
            case TokenType.NUMBER:
                return NumericLiteral(int(self.adv().value))
            
            case TokenType.STRING:
                return StringLiteral(str(self.adv().value))
            
            
            case TokenType.LPAREN:
                self.adv() # consume '('
                value = self.parse_expr()
                self.expect(TokenType.RPAREN) # consume ')'
                return value
            
            case default:
                self.errors.append(f"Unexpected token {self.at().value} at line {self.at().ln}, col {self.at().col}")
                self.adv()
                return None

