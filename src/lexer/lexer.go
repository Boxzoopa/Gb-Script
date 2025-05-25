package lexer

import (
	"regexp"
	"fmt")

type regexHandler func (lexer *lexer, regex *regexp.Regexp) 

type regexPattern struct {
	regex *regexp.Regexp
	handler  regexHandler
}

type lexer struct {
	patterns []regexPattern
	tokens []Token
	srcCode string
	pos int
}

// ==== Lexer Methods ====
func (lex *lexer) adv(n int) {
	lex.pos += n
}

func (lex *lexer) add(token Token) {
	lex.tokens = append(lex.tokens, token)
}

func (lex *lexer) at () byte {
	return lex.srcCode[lex.pos]
}

func (lex *lexer) remainder () string {
	return lex.srcCode[lex.pos:]
}

func (lex *lexer) at_eof () bool {
	return lex.pos >= len(lex.srcCode)
}


func Tokenize(src string) []Token {
	lex := newLexer(src)

	for !lex.at_eof() {
		matched := false

		for _, pattern := range lex.patterns {
			// iterate over every single pattern
			loc := pattern.regex.FindStringIndex(lex.remainder())

			if loc != nil && loc[0] == 0 {
				pattern.handler(lex, pattern.regex)
				matched = true
				break // exit the loop if a pattern matches
			}
		}

		// NOTE:: Extend to print location of error and other useful debugging information
		if !matched {
			panic(fmt.Sprintf("Lexer::Error -> unreckognized token near %s\n", lex.remainder()))
		}
		
	}
	lex.add(newToken(EOF, "EOF")) // add EOF token at the end
	return lex.tokens
}
	

func newLexer(srcCode string) *lexer {
	return &lexer{
		pos:      0,
		srcCode:  srcCode,
		tokens:   make([]Token, 0),
		patterns: []regexPattern{
			// define all the patterns
			{regexp.MustCompile(`[0-9]+(\.[0-9]+)?`), numberHandler},
			{regexp.MustCompile(`\s`), skipHandler}, // skip whitespace
			{regexp.MustCompile(`\(`), defaultHandler(L_PAREN, "(")},
			{regexp.MustCompile(`\)`), defaultHandler(R_PAREN, ")")},
			{regexp.MustCompile(`\{`), defaultHandler(L_CURLY, "{")},
			{regexp.MustCompile(`\}`), defaultHandler(R_CURLY, "}")},
			{regexp.MustCompile(`\[`), defaultHandler(L_BRACK, "[")},
			{regexp.MustCompile(`\]`), defaultHandler(R_BRACK, "]")},
			{regexp.MustCompile(`==`), defaultHandler(ASSIGNMENT, "==")},
			{regexp.MustCompile(`!=`), defaultHandler(NOT_EQ, "!=")},
			{regexp.MustCompile(`=`), defaultHandler(ASSIGN, "=")},
			{regexp.MustCompile(`!`), defaultHandler(NOT, "!")},
			{regexp.MustCompile(`<=`), defaultHandler(LESS_EQ, "<=")},
			{regexp.MustCompile(`<`), defaultHandler(LESS, "<")},
			{regexp.MustCompile(`>=`), defaultHandler(GREATER_EQ, ">=")},
			{regexp.MustCompile(`>`), defaultHandler(GREATER, ">")},
			{regexp.MustCompile(`\|\|`), defaultHandler(OR, "||")},
			{regexp.MustCompile(`&&`), defaultHandler(AND, "&&")},
			{regexp.MustCompile(`\.\.`), defaultHandler(DOT_DOT, "..")},
			{regexp.MustCompile(`\.`), defaultHandler(DOT, ".")},
			{regexp.MustCompile(`;`), defaultHandler(SEMICOLON, ";")},
			{regexp.MustCompile(`:`), defaultHandler(COLON, ":")},
			{regexp.MustCompile(`\?`), defaultHandler(QUESTION, "?")},
			{regexp.MustCompile(`,`), defaultHandler(COMMA, ",")},
			{regexp.MustCompile(`\+\+`), defaultHandler(P_PLUS, "++")},
			{regexp.MustCompile(`--`), defaultHandler(M_DASH, "--")},
			{regexp.MustCompile(`\+=`), defaultHandler(PLUS_EQ, "+=")},
			{regexp.MustCompile(`-=`), defaultHandler(DASH_EQ, "-=")},
			{regexp.MustCompile(`\+`), defaultHandler(PLUS, "+")},
			{regexp.MustCompile(`-`), defaultHandler(DASH, "-")},
			{regexp.MustCompile(`/`), defaultHandler(SLASH, "/")},
			{regexp.MustCompile(`\*`), defaultHandler(STAR, "*")},
			{regexp.MustCompile(`%`), defaultHandler(PERCENT, "%")},
	
		},
	}
}

// ==== Regex Handlers ====

func defaultHandler(kind TokenKind, value string) regexHandler {
	return func(lex *lexer, regex *regexp.Regexp) {
		// advance the lexer's position past the matched token
		lex.adv(len(value))
		lex.add(newToken(kind, value))
	}
	
}

func numberHandler(lex * lexer, regex *regexp.Regexp) {
	match := regex.FindString(lex.remainder())
	lex.add(newToken(NUMBER, match))
	lex.adv(len(match))

}

func skipHandler(lex * lexer, regex *regexp.Regexp) {
	match := regex.FindStringIndex(lex.remainder())
	lex.adv(match[1])

}

