# parser.py
from src.tokens import TokenType, Token
from src.nodes import *

PRECEDENCE = {
    TokenType.SEMICOLON: -1,
    TokenType.COMMA: -1,
    TokenType.ASSIGN: 1,
    TokenType.EQUALS: 2,
    TokenType.NOT_EQ: 2,
    TokenType.OR: 3,
    TokenType.AND: 4,
    TokenType.PLUS: 10,
    TokenType.MINUS: 10,
    TokenType.MULT: 20,
    TokenType.DIV: 20,
    TokenType.LPAREN: 0,
    TokenType.RPAREN: 0,
}


prgm_vars = []
prgm_grps = []

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # === Utility Methods ===

    def advance(self):
        tok = self.current()
        self.pos += 1
        return tok

    def current(self):
        if self.pos >= len(self.tokens):
            return Token(TokenType.EOF, "")
        return self.tokens[self.pos]

    def expect(self, kind):
        if self.current().kind != kind:
            raise Exception(f"Expected token {kind}, but got {self.current().kind}")
        return self.advance()

    def peek(self, offset=1):
        if self.pos + offset >= len(self.tokens):
            return Token(TokenType.EOF, "")
        return self.tokens[self.pos + offset]


    def nud(self, token):
        if token.kind == TokenType.NUMBER:
            return NumberNode(token.value).to_dict()
        elif token.kind == TokenType.MINUS:
            right = self.parse_expr(PRECEDENCE[TokenType.MINUS])
            return UnaryOpNode(token.value, right).to_dict()
        # Add other prefix cases here...

        elif token.kind == TokenType.LPAREN:
            # Parse inside with precedence higher than RPAREN's to stop at ')'
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN)
            return GroupedNode(expr).to_dict()
        
        elif token.kind == TokenType.STRING:
            return StringNode(token.value).to_dict()


    def led(self, token, left):
        if token.kind == TokenType.PLUS:
            right = self.parse_expr(PRECEDENCE[TokenType.PLUS]- 1)
            return BinaryOpNode(left, token.value, right).to_dict()
        elif token.kind == TokenType.MINUS:
            right = self.parse_expr(PRECEDENCE[TokenType.MINUS]- 1)
            return BinaryOpNode(left, token.value, right).to_dict()
        elif token.kind == TokenType.MULT:
            right = self.parse_expr(PRECEDENCE[TokenType.MULT]- 1)
            return BinaryOpNode(left, token.value, right).to_dict()
        elif token.kind == TokenType.DIV:
            right = self.parse_expr(PRECEDENCE[TokenType.DIV]- 1)
            return BinaryOpNode(left, token.value, right).to_dict()
        # Add other infix cases here...

        elif token.kind == TokenType.LBRAC:
            index_expr = self.parse_expr()
            self.expect(TokenType.RBRAC)
            return IndexNode(left, index_expr).to_dict()



    # === Parsing Methods ===

    def parse(self):
        statements = []
        while self.current().kind != TokenType.EOF:
            stmt = self.parse_stmt()
            statements.append(stmt)
        return ProgramNode(statements).to_dict()

    def parse_stmt(self):
        tok = self.current()

        if tok.kind == TokenType.VAR or tok.kind == TokenType.CONST:
            name = self.peek(1)
            if name.kind == TokenType.IDENT:
                if name.value in prgm_vars:
                    raise Exception(f"Variable '{name.value}' already declared.")
            if tok.kind == TokenType.VAR:
                return self.parse_var_decl(is_const=False)
            elif tok.kind == TokenType.CONST:
                return self.parse_var_decl(is_const=True)
            
        
        if tok.kind == TokenType.GRP:
            name = self.peek(1)
            if name.kind == TokenType.IDENT:
                if name.value in prgm_grps:
                    raise Exception(f"Group '{name.value}' already declared.")
                
                return self.parse_group_decl()
            

        else:
            expr = self.parse_expr()
            self.expect(TokenType.SEMICOLON)
            return ExpressionNode(expr).to_dict()


    def parse_expr(self, precedence=0):
        tok = self.current()
        left = self.nud(tok)
        self.advance()  # Consume the token

        while precedence < PRECEDENCE.get(self.current().kind, 0):
            tok = self.advance()
            left = self.led(tok, left)

        return left
    
        # === Variable Declaration ===
    def parse_var_decl(self, is_const):
        self.advance()  # Consume VAR or CONST

        name_tok = self.expect(TokenType.IDENT)
        name = name_tok.value
        init = None

        var_type = None
        if self.current().kind == TokenType.COLON:
            self.advance()
            if self.current().kind == TokenType.INT:
                type_tok = self.expect(TokenType.INT)
            elif self.current().kind == TokenType.STR:
                type_tok = self.expect(TokenType.STR)
            else:
                raise Exception(f"Expected type after ':', but got {self.current().kind}")
            var_type = type_tok.value
        
        init = None
        if is_const:
            if self.current().kind != TokenType.ASSIGN:
                raise Exception(f"Constant '{name}' must be initialized at declaration.")


        if self.current().kind == TokenType.ASSIGN:
            self.advance()
            init = self.parse_expr()

            if init is not None and var_type is not None:
                if init['type'] == TokenType.NUMBER and var_type != "int":
                    raise Exception(f"Type mismatch: '{name}' expected {var_type}, but got {init['type']}")
                elif init['type'] == TokenType.STRING and var_type != "str":
                    raise Exception(f"Type mismatch: '{name}' expected {var_type}, but got {init['type']}")



        self.expect(TokenType.SEMICOLON)
        prgm_vars.append(name)
        #print(prgm_vars)
        return VarDeclNode(name, init, is_const, var_type).to_dict()


    # === Group Declaration ===
    def parse_group_decl(self):
        self.advance()  # Consume GRP

        name_tok = self.expect(TokenType.IDENT)
        name = name_tok.value

        self.expect(TokenType.COLON)
        if self.current().kind == TokenType.INT:
            type_tok = self.expect(TokenType.INT)
        elif self.current().kind == TokenType.STR:
            type_tok = self.expect(TokenType.STR)
        else:
            raise Exception(f"Expected type after ':', but got {self.current().kind}")
        var_type = type_tok.value

        self.expect(TokenType.ASSIGN)  # <-- Make sure you consume the '=' here
        self.expect(TokenType.LBRAC)  # <-- Make sure you consume the '[' here

        elements = []
        index = 0
        while self.current().kind != TokenType.RBRAC:
            expr = self.parse_expr()
            node = IndexNode(name, index, expr).to_dict()

            elements.append(node)

            if self.current().kind == TokenType.COMMA:
                self.advance()  # Skip comma if present
            
            index += 1

        self.expect(TokenType.RBRAC)
        self.expect(TokenType.SEMICOLON)
        prgm_grps.append(name)

        return GrpDeclNode(name, elements, var_type).to_dict()
