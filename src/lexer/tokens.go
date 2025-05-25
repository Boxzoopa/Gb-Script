package lexer


import "fmt"

type TokenKind int

const (
	EOF TokenKind = iota
	NUMBER
	STRING
	IDENT
	NULL

	L_PAREN
	R_PAREN
	L_BRACK
	R_BRACK
	L_CURLY
	R_CURLY

	ASSIGN // =
	ASSIGNMENT // ==
	NOT // !
	NOT_EQ

	LESS
	LESS_EQ
	GREATER
	GREATER_EQ

	OR
	AND

	DOT
	DOT_DOT
	SEMICOLON
	COLON
	COMMA
	QUESTION

	PLUS
	DASH
	STAR
	SLASH
	PERCENT // %
	POW // ^

	P_PLUS // ++
	M_DASH
	PLUS_EQ // +=
	DASH_EQ
	STAR_EQ
	SLASH_EQ


	// reserved keywords
	VAR
	CONST
	OBJ
	GRP
	FUN
	IMPORT
	RETURN
	IF
	ELSE
	FOR
	WHILE
	TYPEOF
	IN
	TRUE
	FALSE
	NEW
	FROM
	FUNC
)

type Token struct {
	kind TokenKind
	value string
}

func (token Token) matches (expectedTokens ...TokenKind) bool {
	for _, expected := range expectedTokens {
		if expected == token.kind {
			return true
		}
	}
	return false
}

func (token Token) Debug() {
	if token.matches(IDENT, NUMBER, STRING) {
		fmt.Printf("Token: %s (%s)\n", tokenKindString(token.kind), token.value)
	} else {
		fmt.Printf("Token: %s ()\n", tokenKindString(token.kind))
	}
}

func newToken(kind TokenKind, value string) Token {
	return Token {
		kind:  kind,
		value: value,
	}
}


func tokenKindString(kind TokenKind) string {
	switch kind {
	case EOF:
		return "eof"
	case NULL:
		return "null"
	case NUMBER:
		return "number"
	case STRING:
		return "string"
	case TRUE:
		return "true"
	case FALSE:
		return "false"
	case IDENT:
		return "identifier"
	case L_PAREN:
		return "open_paren"
	case R_PAREN:
		return "close_paren"
	case L_CURLY:
		return "open_curly"
	case R_CURLY:
		return "close_curly"
	case L_BRACK:
		return "open_bracket"
	case R_BRACK:
		return "close_bracket"
	case ASSIGN:
		return "assignment"
	case ASSIGNMENT:
		return "equals"
	case NOT_EQ:
		return "not_equals"
	case NOT:
		return "not"
	case LESS:
		return "less"
	case LESS_EQ:
		return "less_equals"
	case GREATER:
		return "greater"
	case GREATER_EQ:
		return "greater_equals"
	case OR:
		return "or"
	case AND:
		return "and"
	case DOT:
		return "dot"
	case DOT_DOT:
		return "dot_dot"
	case SEMICOLON:
		return "semicolon"
	case COLON:
		return "colon"
	case QUESTION:
		return "question"
	case COMMA:
		return "comma"
	case P_PLUS:
		return "plus_plus"
	case M_DASH:
		return "minus_minus"
	case PLUS_EQ:
		return "plus_equals"
	case DASH_EQ:
		return "minus_equals"
	case PLUS:
		return "plus"
	case DASH:
		return "minus"
	case SLASH:
		return "slash"
	case STAR:
		return "star"
	case PERCENT:
		return "percent"
	case POW:
		return "power"
	case VAR:
		return "var"
	case CONST:
		return "const"
	case OBJ:
		return "object"
	case NEW:	
		return "new"
	case IMPORT:
		return "import"
	case FROM:
		return "from"
	case FUNC:
		return "func"
	case IF:
		return "if"
	case ELSE:
		return "else"
	case FOR:
		return "for"
	case WHILE:
		return "while"
	case IN:
		return "in"
	default:
		return fmt.Sprintf("unknown(%d)", kind)
	}
}