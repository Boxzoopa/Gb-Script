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
    "postfix": (TokenType.P_PLUS, TokenType.M_MINUS),
    "call": (TokenType.LPAREN, TokenType.DOT),
    "primary": (TokenType.IDENT, TokenType.NUMBER, TokenType.STRING, TokenType.NULL, TokenType.MODULE),
    "speical": {TokenType.SPRITE}
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
            if type_name not in ("int", "str", "object", "sprite"):
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
            
            case TokenType.FUNC:
                return self.parse_func_decl()

            case TokenType.STATE:
                return self.parse_state()
            
            case TokenType.RETURN:
                return self.parse_return()
            
            case TokenType.IF:
                return self.parse_if()
            
            case TokenType.WHILE:
                return self.parse_while()
            
            case TokenType.FOR:
                return self.parse_for()
            
            case TokenType.MODULE:
                return self.parse_primary()

            case default:

                expr = self.parse_expr()

                # If it looks like an assignment (e.g. `a = b` or `a.b = c`)
                if self.at().type in PRECEDENCE["assignment"]:
                    op_token = self.adv().value  # ← capture the actual operator token
                    value = self.parse_expr()
                    self.expect(TokenType.SEMICOLON)
                    return AssignmentExpr(expr, value, op_token)

                self.expect(TokenType.SEMICOLON)
                return expr

    # Statements
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

            return VariableDeclaration(
                name, is_const=is_const, value=None, explicit_type=type_name
            )
        
        self.expect(TokenType.ASSIGNMENT)
        assigned_value = self.parse_expr()

        self.expect(TokenType.SEMICOLON)

        return VariableDeclaration(
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
            return GroupDeclaration(name, group_type, size)
        
        self.expect(TokenType.ASSIGNMENT)
        self.expect(TokenType.LBRAC)
        items = []
        index = 0

        while self.at().type != TokenType.RBRAC:
            i = self.parse_expr()
            item = IndexLiteral(index, i)
            items.append(item)
            index += 1

            if self.at().type == TokenType.COMMA:
                self.adv()


        self.expect(TokenType.RBRAC)
        self.expect(TokenType.SEMICOLON)
        return GroupDeclaration(name, group_type, size, items)

    def parse_object_decl(self):
        self.adv()

        name = self.expect(TokenType.IDENT).value

        if self.at().type == TokenType.LCURL:
            self.adv()
            properties = []

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

        # handle object assignment obj x = rect {}
        elif self.at().type == TokenType.ASSIGNMENT:
            self.adv()
            expr = ObjectLiteral(self.adv().value)
            self.expect(TokenType.LCURL)
            self.expect(TokenType.RCURL)
            self.expect(TokenType.SEMICOLON)
            return VariableDeclaration(name, value=expr, explicit_type="object")

        else:
            self.errors.append(f"Expected '{{' or '=' after object name '{name}' at line {self.at().ln}, col {self.at().col}")
            return None

    def parse_func_decl(self):
        self.adv()
        name = self.expect(TokenType.IDENT).value
        params = self.parse_func_params()
        return_type = None

        if self.at().type == TokenType.COLON:
            self.adv()
            return_type = self.get_type()
            if return_type == "object":
                self.expect(TokenType.LPAREN)
                return_type = self.adv().value
                self.expect(TokenType.RPAREN)

        self.expect(TokenType.LCURL)
        body : List[Stmt] = []

        while self.not_at_end() and self.at().type != TokenType.RCURL:
            stmt = self.parse_stmt()
            body.append(stmt)
        
        self.expect(TokenType.RCURL)
        return FunctionDeclaration(name, params, body, return_type)
    
    def parse_state(self):
        self.adv()
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.LPAREN)
        self.expect(TokenType.RPAREN)

        self.expect(TokenType.LCURL)
        body : List[Stmt] = []

        while self.not_at_end() and self.at().type != TokenType.RCURL:
            stmt = self.parse_stmt()
            body.append(stmt)
        
        self.expect(TokenType.RCURL)

        return StateDeclaration(name, body)
    
    def parse_func_params(self):
        self.expect(TokenType.LPAREN)
        params = []

        if self.at().type == TokenType.RPAREN:
            self.adv()
            return params

        while True:
            name = self.expect(TokenType.IDENT).value
            self.expect(TokenType.COLON)
            type_ = self.get_type()
            params.append(Property(name, type_))

            if self.at().type == TokenType.COMMA:
                self.adv()
            else:
                break

        self.expect(TokenType.RPAREN)
        return params

    def parse_return(self):
        self.adv()
        value = self.parse_expr()
        self.expect(TokenType.SEMICOLON)
        return ReturnStmt(value)

    def parse_if(self):
        self.adv()
        conditions = []
        self.expect(TokenType.LPAREN)

        while self.at().type != TokenType.RPAREN:
            condition = self.parse_expr()
            conditions.append(condition)

            if self.at().type == TokenType.COMMA:
                self.adv()
            else:
                break
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LCURL)
        then_branch = []
        elif_branches = []
        else_branch = []

        while self.not_at_end() and self.at().type != TokenType.RCURL:
            stmt = self.parse_stmt()
            if stmt:
                then_branch.append(stmt)

        self.expect(TokenType.RCURL)

        if self.at().type == TokenType.ELIF:
            elif_branches.append(self.parse_if())
        
        if self.at().type == TokenType.ELSE:
            self.adv()
            self.expect(TokenType.LCURL)
            while self.not_at_end() and self.at().type != TokenType.RCURL:
                stmt = self.parse_stmt()
                if stmt:
                    else_branch.append(stmt)
            self.expect(TokenType.RCURL)


        return IfStmt(conditions, then_branch, elif_branches, else_branch)

    def parse_while(self):
        self.adv()
        self.expect(TokenType.LPAREN)
        condition = self.parse_expr()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LCURL)
        body = []

        while self.not_at_end() and self.at().type != TokenType.RCURL:
            stmt = self.parse_stmt()
            if stmt:
                body.append(stmt)

        self.expect(TokenType.RCURL)

        return WhileStmt(condition, body)

    def parse_for(self):
        self.adv()
        self.expect(TokenType.LPAREN)
        init = None

        if self.at().type == TokenType.VAR:
            init = self.parse_var_decl()
        
        condition = None
        while self.at().type != TokenType.SEMICOLON:
            if condition is None:
                condition = self.parse_expr()
            else:
                self.errors.append(f"Unexpected token {self.at().value} in for loop condition at line {self.at().ln}, col {self.at().col}")
                self.adv()
        self.expect(TokenType.SEMICOLON)

        increment = None
        if self.at().type != TokenType.RPAREN:
            increment = self.parse_expr()
            if self.at().type != TokenType.RPAREN:
                self.errors.append(f"Expected ')' after for loop increment at line {self.at().ln}, col {self.at().col}")
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LCURL)
        body = []
        while self.not_at_end() and self.at().type != TokenType.RCURL:
            stmt = self.parse_stmt()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RCURL)
        return ForStmt(init, condition, increment, body)

    # Other Precedence Parsing Methods
    def parse_expr(self):
        return self.parse_logical()
    
    def parse_logical(self):
        left = self.parse_relational()
        while self.at().type in PRECEDENCE["logical"]:
            op = self.adv().value
            right = self.parse_relational()
            left = BinaryExpr(left, right, op)
        return left

    def parse_relational(self):
        left = self.parse_additive()
        while self.at().type in PRECEDENCE["relational"]:
            op = self.adv().value
            right = self.parse_additive()
            left = BinaryExpr(left, right, op)
        return left

    def parse_assignment(self):
        left  = self.parse_additive()

        if self.at().type in PRECEDENCE["assignment"]: # =
            op = self.adv().value # consume '=', '+=', '-=', etc.
            value = self.parse_assignment()
            return AssignmentExpr(left, value, op)
        
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
        if self.at().type in PRECEDENCE["unary"]:
            op = self.adv().value
            operand = self.parse_unary()  # recursive to support chains like --x
            return UnaryExpr(operand, op)
        return self.parse_postfix()
    
    def parse_postfix(self):
        expr = self.parse_call_member()  # `a`, `a.b`, `a[0]`, etc.

        while self.at().type in PRECEDENCE["postfix"]:
            op = self.adv().value  # ++ or --
            expr = UnaryExpr(expr, op, postfix=True)

        return expr


    # Call/Member Parsing
    def parse_call_member(self):
        member = self.parse_member()

        if self.at().type == TokenType.LPAREN:  # function call
            return self.parse_call(member)
        
        return member

    def parse_call(self, caller):
        call_expr = CallExpr(caller, self.parse_args())

        if self.at().type == TokenType.LPAREN:
            call_expr = self.parse_call(call_expr)

        return call_expr
    
    def parse_args(self):
        self.expect(TokenType.LPAREN)  # consume '('

        if self.at().type == TokenType.RPAREN:
            args = []
        else:
            args = self.parse_args_list()

        self.expect(TokenType.RPAREN)  # consume ')'
        return args
    
    def parse_args_list(self):
        args = [self.parse_expr()]

        while (self.not_at_end() and self.at().type == TokenType.COMMA and self.adv()):
            args.append(self.parse_expr())

        return args

    def parse_member(self):
        object_ = self.parse_primary()

        while self.at().type in (TokenType.DOT, TokenType.LBRAC):
            operator = self.adv()
            property_ = None
            computed = None

            if operator.type == TokenType.DOT:
                computed = False
                property_ = self.parse_primary()

                if property_ is None or not isinstance(property_, Identifier):
                    self.errors.append(f"Expected identifier after '.' at line {self.at().ln}, col {self.at().col}")
                    return None
            else:
                computed = True
                property_ = self.parse_expr()  # parse expression for computed property
                self.expect(TokenType.RBRAC)  # consume ']'
        
            object_ = MemberExpr(object_, property_, computed)
            
        return object_


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
            
            case TokenType.MODULE:
                self.adv()
                self.expect(TokenType.LPAREN)
                mod_name = self.expect(TokenType.STRING).value
                self.expect(TokenType.RPAREN)
                return ModuleNode(mod_name)
    
            case TokenType.LPAREN:
                self.adv() # consume '('
                value = self.parse_expr()
                self.expect(TokenType.RPAREN) # consume ')'
                return value
            
            case default:
                self.errors.append(f"Unexpected token {self.at().value} at line {self.at().ln}, col {self.at().col}")
                self.adv()
                return None

        

sprite_counter = 0
