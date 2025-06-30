import ply.lex as lex
from tokens import tokens

class LexicalAnalyzer:
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

    tokens = tokens

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

    t_ignore = ' \t\r'

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.errors = []

    def t_COMMENT(self, t):
        r'/\*([^*]|\*+[^*/])*\*/'
        pass  # Ignora comentários

    def t_STR(self, t):
        r'"([^\"]|\\\")*"'
        t.value = t.value[1:-1]
        return t

    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_BOOL(self, t):
        r'verdadeiro|falso'
        t.value = True if t.value.lower() == 'verdadeiro' else False
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value.lower(), 'ID')
        return t

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1

    def t_errcomment(self, t):
        r'/\*([^*]|\*+[^*/])'
        msg = f"Comentário não fechado: '{t.value[0]}' na linha {t.lineno}"
        self.errors.append(msg)
        print(msg)
        t.lexer.skip(1)
                     
    def t_errstr(self, t):
        r'"([^*]|\*+[^*/])'
        msg = f"String não fechada: '{t.value[0]}' na linha {t.lineno}"
        self.errors.append(msg)
        print(msg)
        t.lexer.skip(1)

    def t_error(self, t):
        msg = f"Caractere ilegal: '{t.value[0]}' na linha {t.lineno}"
        self.errors.append(msg)
        print(msg)
        t.lexer.skip(1)

    def tokenize_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        return self.tokenize(data)

    def tokenize(self, input_string):
        print("Análise léxica:")
        self.errors = []
        self.lexer.input(input_string)
        tokens_list = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens_list.append(tok)
        print("Fim da análise léxica.")
        return tokens_list
