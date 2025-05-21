# tokens.py

class TokenType:
    # Identifiers & literals
    IDENT = "identifier"
    NUMBER = "number"
    STRING = "string"

    # Operators
    PLUS = "plus"
    MINUS = "minus"
    MULT = "multiply"
    DIV = "divide"
    POW = "power"

    ASSIGN = "assignment" # =
    EQUALS = "equals" # ==
    NOT = "not" # !
    NOT_EQ = "not_equals" # !=
    OR = "or" 
    AND = "and" 
    P_PLUS = "plus_plus" # ++
    M_MINUS = "minus_minus" # --
    P_EQ = "plus_eq" # +=
    M_EQ = "minus_eq" # -=


    # Delimiters
    SEMICOLON = "semicolon"
    COLON = "colon"
    QUESTION = "question_mark"
    COMMA = "comma"
    LPAREN = "l_paren"
    RPAREN = "r_paren"
    LBRAC = "l_brace"
    RBRAC = "r_brace"
    LCURL = "l_curl"
    RCURL = "r_curl"

    # Special
    EOF = "eof"

    # Reserved Keywords
    VAR = "var"
    CONST = "const"
    NEW = "new"
    FUNC = "func"
    OBJECT = "obj"
    IF = "if"
    ELSE ="else"
    ELSEIF ="else_if"
    WHILE ="while"
    FROM ="from"
    IMPORT = "import"
    IN = "in"
    OR = "or"
    TRUE = "true"
    FALSE = "false"
        # Type Keywords
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STR = "str"
    GRP = "grp"



class Token:
    def __init__(self, kind: TokenType, value: str):
        self.kind = kind
        self.value = value

    def __repr__(self):
        if match_toks(self, [TokenType.IDENT, TokenType.NUMBER, TokenType.STRING]):
            return f"Token({self.kind}, {self.value})"
        else:
            return f"Token({self.kind})"


def match_toks(token: Token, expected_tokens: list[TokenType]) -> bool:
    for expected in expected_tokens:
        if expected == token.kind:
            return True
    return False