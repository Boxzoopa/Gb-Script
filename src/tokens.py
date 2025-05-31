# tokens.py
from typing import Type

class TokenType:
     # Identifiers & literals
    IDENT = "identifier"
    NUMBER = "number"
    STRING = "string"
    NULL = "null" # null literal
    EOF = "eof"

    LPAREN = "l_paren" # (
    RPAREN = "r_paren" # )
    LBRAC = "l_bracket" # [
    RBRAC = "r_bracket" # ]
    LCURL = "l_curl" # {
    RCURL = "r_curl" # }

    # Operators
    PLUS = "plus"
    DASH = "dash"
    STAR = "star"
    SLASH = "slash"
    PERCENT = "percent"

    ASSIGNMENT = "assignment" # =
    EQUALS = "equals" # ==
    NOT = "not" # !
    NOT_EQ = "not_equals" # !=
    LESS = "less"
    LESS_EQ = "less_eq"
    GREATER = "greater"
    GREATER_EQ = "greater_eq"

    OR = "or" 
    AND = "and" 

    # Delimiters
    SEMICOLON = "semicolon"
    COLON = "colon"
    QUESTION = "question_mark"
    DOT = "dot"
    COMMA = "comma"
    P_PLUS = "plus_plus" # ++
    M_MINUS = "minus_minus" # --
    PLUS_EQ = "plus_eq" # +=
    MINUS_EQ = "minus_eq" # -=

    # Reserved Keywords
    VAR = "var"
    CONST = "const"
    OBJ = "obj"
    STATE = "state"
    GRP = "grp"
    SPRITE = "spr"
    NEW = "new"
    MODULE = "module"
    IMPORT = "import"
    FROM ="from"
    FUNC = "func"
    IF = "if"
    ELIF = "elif"
    ELSE ="else"
    WHILE ="while"
    FOR ="for"
    IN = "in"
    RETURN = "return"


class Token:
    def __init__(self, type : TokenType, value : str, ln : int = 0, col : int = 0):
        self.type = type
        self.value = value
        self.ln = ln
        self.col = col

    def __repr__(self):
        if match_toks(self, [TokenType.IDENT, TokenType.NUMBER, TokenType.STRING]):
            return f"{self.type}({self.value})" #, ln={self.line}, col={self.column})"
        else:
            return f"{self.type}()" #, ln={self.line}, col={self.column})"


def match_toks(token: Token, expected_tokens: list[TokenType]) -> bool:
    for expected in expected_tokens:
        if expected == token.type:
            return True
        
    return False
