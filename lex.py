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
    '.': 'DOT',
    'Ler': 'LER',
    'Escrever': 'ESCREVER',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'enquanto': 'ENQUANTO',
    'faca': 'FACA',
}

tokens = [
    'ID', 'NUM', 'STR',
    'MAIS', 'MENOS', 'VEZES', 'DIV',
    'ATRIB', 'IGUAL', 'DIF', 'MENOR', 'MENORIG', 'MAIOR', 'MAIORIG',
    'LPAREN', 'RPAREN', 'SEMI', 'COLON', 'COMMA', 'COMMENT',
] + list(reserved.values())

# Expressões regulares para tokens simples

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','
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
t_DOT = r'\.'

def t_COMMENT(t):
    r'/\*([^*]|\*+[^*/])*\*/'
    pass  # Ignora comentários

def t_STR(t):
    r'"([^\"]|\\\")*"'
    t.value = t.value[1:-1]
    return t

def t_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore = ' \t\r\n'

def t_error(t):
    print(t)
    raise Exception(f"Caractere ilegal: {t.value[0]}")

def tokenize(input_string):
    lexer = lex.lex()
    lexer.input(input_string)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append((tok.type, tok.value))
    return tokens_list
