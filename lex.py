import ply.lex as lex
import re

# Lista de tokens
reserved = {
    'programa': 'PROGRAMA',
    'var': 'VAR',
    'inteiro': 'INTEIRO',
    'logico': 'LOGICO',
    'inicio': 'INICIO',
    'fim': 'FIM',
    'ler': 'LER',
    'escrever': 'ESCREVER',
    'senao': 'SENAO',
    'entao': 'ENTAO',
    'se': 'SE',
    'enquanto': 'ENQUANTO',
    'faca': 'FACA',
}

tokens = [
    'ID', 'NUM', 'STR', 'BOOL',
    'MAIS', 'MENOS', 'VEZES', 'DIV',
    'ATRIB', 'IGUAL', 'DIF', 'MENOR', 'MENORIG', 'MAIOR', 'MAIORIG',
    'LPAREN', 'RPAREN', 'SEMI', 'COLON', 'COMMA', 'DOT',
    'OR', 'AND', 'NOT'
] + list(reserved.values())


# Expressões regulares para tokens simples
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_MAIS = r'\+'
t_MENOS = r'-'
t_VEZES = r'\*'
t_DIV = r'/'
t_ATRIB = r':='
t_IGUAL = r'='
t_DIF = r'<>'
t_MENORIG = r'<='
t_MAIORIG = r'>='
t_MENOR = r'<'
t_MAIOR = r'>'
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'

def t_COMMENT(t):
    r'/\*([^*]|\*+[^*/])*\*/'
    pass  # Ignora comentários

def t_STR(t):
    r'"([^\"]|\\\")*"'
    t.value = t.value[1:-1]
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'(?i)verdadeiro|falso'
    t.value = True if t.value.lower() == 'verdadeiro' else False
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Palavras reservadas devem ser comparadas em minúsculo
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]} na linha {t.lineno}")
    raise Exception(f"Caractere ilegal: {t.value[0]} na linha {t.lineno}")

def tokenize(input_string):
    lexer = lex.lex()
    tokens_list = []
    lines = input_string.split('\n')
    for line in lines:
        lexer.input(line)
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens_list.append((tok.type, tok.value))
    return tokens_list
