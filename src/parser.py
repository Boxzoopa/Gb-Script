from src.nodes import *
from src.tokens import Token, TokenType

## Precedence Levels Reference, Lowest to Highest
PRECEDENCE = {
    "default": (TokenType.SEMICOLON, TokenType.EOF),
    "comma": (TokenType.COMMA,),
    "assignment": (TokenType.ASSIGNMENT, TokenType.PLUS_EQ, TokenType.MINUS_EQ),
    "logical": (TokenType.AND, TokenType.OR),
    "relational": (TokenType.EQUALS, TokenType.NOT_EQ,
                   TokenType.GREATER, TokenType.GREATER_EQ,
                   TokenType.LESS, TokenType.LESS_EQ),
    "additive": (TokenType.PLUS, TokenType.DASH),
    "multiplicative": (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT),
    "unary": (TokenType.DASH, TokenType.NOT, TokenType.PLUS),
    "call": (TokenType.LPAREN, TokenType.DOT),
    "primary": (TokenType.IDENT, TokenType.NUMBER, TokenType.STRING, TokenType.NULL),
}

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
    
    def get_type(self):
        if self.at().type == TokenType.IDENT:
            type_name = self.adv().value
            if type_name not in ("int", "str", "bool", "float"):
                self.errors.append(f"Unsupported type '{type_name}' at line {self.at().ln}, col {self.at().col}")
                return None
            return type_name
        else:
            self.errors.append(f"Expected type identifier at line {self.at().ln}, col {self.at().col}")
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
            
            case TokenType.GRP:
                return self.parse_group_decl()
            
            case TokenType.OBJ:
                return self.parse_object_decl()
            
            case default:
                expr = self.parse_expr()
                self.expect(TokenType.SEMICOLON)
                return expr

    def parse_expr(self):
        return self.parse_assignment()

    def parse_var_decl(self):
        is_const = self.adv().type == TokenType.CONST
        name = self.expect(TokenType.IDENT).value
        type_name = None

        if self.at().type == TokenType.COLON:
            self.adv()
            type_name = self.get_type()

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

    def parse_group_decl(self):
        self.adv()
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.COLON)
        group_type = self.get_type()
        self.expect(TokenType.LBRAC)
        size = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.RBRAC)

        if self.at().type == TokenType.SEMICOLON:
            self.adv()
            return GroupDecleration(name, group_type, size)
        
        self.expect(TokenType.ASSIGNMENT)
        self.expect(TokenType.LBRAC)
        items = []
        index = 0

        while self.at().type != TokenType.RBRAC:
            i = self.parse_expr()
            item = IndexLiteral(index, i)
            items.append(item)

            if self.at().type == TokenType.COMMA:
                self.adv()
                index += 1

        self.expect(TokenType.RBRAC)
        self.expect(TokenType.SEMICOLON)
        return GroupDecleration(name, group_type, size, items)

    def parse_object_decl(self):
        self.adv()
        name = self.expect(TokenType.IDENT).value
        properties = []
        self.expect(TokenType.LCURL)
        while self.at().type != TokenType.RCURL:
            prop_name = self.expect(TokenType.IDENT).value
            self.expect(TokenType.COLON)
            prop_type = self.get_type()
            properties.append(Property(prop_name, prop_type))
            if self.at().type == TokenType.COMMA:
                self.adv()
        
        self.expect(TokenType.RCURL)
        self.expect(TokenType.SEMICOLON)
        return ObjectDeclaration(name, properties)

    def parse_assignment(self):
        left  = self.parse_additive()

        if self.at().type in PRECEDENCE["assignment"]: # =
            self.adv()  # consume '='
            value = self.parse_assignment()
            return AssignmentExpr(left, value)
        
        return left



    def parse_additive(self):
        left = self.parse_multiplicitave()

        while self.at().type in (TokenType.PLUS, TokenType.DASH):
            op = self.adv().value
            right = self.parse_multiplicitave()
            left = BinaryExpr(left, right, op)

        return left

    def parse_multiplicitave(self):
        left = self.parse_unary()

        while self.at().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.adv().value
            right = self.parse_primary()
            left = BinaryExpr(left, right, op)

        return left

    def parse_unary(self):
        if self.at().type in (TokenType.DASH, TokenType.NOT, TokenType.PLUS):
            op = self.adv().value
            operand = self.parse_unary()  # recursive to support chains like --x
            return UnaryExpr(operand, op)
        return self.parse_primary()

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

