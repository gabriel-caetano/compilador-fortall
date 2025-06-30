import ply.yacc as yacc
from tokens import tokens as tk

class ASTNode:
    def __init__(self, type_, children=None, value=None):
        self.type = type_
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        return f"ASTNode(type={self.type}, value={self.value})\nchildren=[\n{self.children}\n]"

class SyntaxAnalyzer:
    tokens = tk
    def __init__(self):
         self.parser = yacc.yacc(module=self, start='PROG', debug=False, write_tables=False)

    def parse(self, tokens):
        print("Análise sintática:")
        ast = self.parser.parse(lexer=TokenListLexer(tokens))
        print("Fim da análise sintática.")
        return ast

    # Precedência dos operadores
    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('left', 'MENOR', 'MENORIG', 'MAIOR', 'MAIORIG', 'IGUAL', 'DIF'),
        ('left', 'MAIS', 'MENOS'),
        ('left', 'VEZES', 'DIV'),
        ('right', 'UMINUS'),
    )

    def p_prog(self, p):
        'PROG : PROGRAMA ID SEMI DECLARACOES COMPOSTO DOT'
        p[0] = ASTNode('PROG', [p[4], p[5]], value=p[2])

    def p_declaracoes(self, p):
        '''DECLARACOES : DECLARACAO _DECLARACAO
                      | '''
        if len(p) == 3:
            # p[1] é uma declaração, p[2] é uma lista de declarações
            p[0] = ASTNode('DECLARACOES', [p[1]] + p[2])
        else:
            p[0] = ASTNode('DECLARACOES', [])

    def p_declaracao(self, p):
        'DECLARACAO : VAR ID _ID COLON TIPO SEMI'
        p[0] = ASTNode('DECLARACAO', [[p[2]] + p[3], p[5]])

    def p__declaracao(self, p):
        '''_DECLARACAO : DECLARACAO _DECLARACAO
                      | '''
        if len(p) == 3:
            # p[1] é uma declaração, p[2] é uma lista de declarações
            p[0] = [p[1]] + p[2]
        else:
            p[0] = []

    def p_tipo(self, p):
        '''TIPO : INTEIRO
               | LOGICO'''
        p[0] = ASTNode('TIPO', value=p[1])

    def p__id(self, p):
        '''_ID : COMMA ID _ID
               | '''
        if len(p) == 4:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = []

    def p_composto(self, p):
        'COMPOSTO : INICIO COMANDOS FIM'
        p[0] = ASTNode('COMPOSTO', [p[2]])

    def p_comandos(self, p):
        '''COMANDOS : COMANDO SEMI _COMANDO
                    | '''
        if len(p) == 4:
            p[0] = ASTNode('COMANDOS', [p[1], p[3]])
        else:
            p[0] = ASTNode('COMANDOS')

    def p__comando(self, p):
        '''_COMANDO : COMANDO SEMI _COMANDO
                    | '''
        if len(p) == 4:
            p[0] = ASTNode('_COMANDO', [p[1], p[3]])
        else:
            p[0] = ASTNode('_COMANDO')

    def p_comando(self, p):
        '''COMANDO : ATRIBUICAO
                   | LEITURA
                   | ESCRITA
                   | COMPOSTO
                   | CONDICIONAL
                   | REPETICAO'''
        p[0] = p[1]

    def p_atribuicao(self, p):
        '''ATRIBUICAO : ID ATRIB EXPR
                    | ID ATRIB EXPR_LOGICA'''
        p[0] = ASTNode('ATRIBUICAO', [p[3]], value=p[1])

    def p_leitura(self, p):
        'LEITURA : LER LPAREN ID _ID RPAREN'
        # Garante que todos os parâmetros sejam ASTNode do tipo ID
        ids = [ASTNode('ID', value=p[3])] + [ASTNode('ID', value=x) for x in p[4]]
        p[0] = ASTNode('LEITURA', ids)

    def p_escrita(self, p):
        'ESCRITA : ESCREVER LPAREN ESPR_STR RPAREN'
        p[0] = ASTNode('ESCRITA', [p[3]])

    def p_espr_str(self, p):
        '''ESPR_STR : ITEM_ESCRITA _ITEM_ESCRITA
                    | '''
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = []

    def p_item_escrita(self, p):
        '''ITEM_ESCRITA : EXPR
                       | EXPR_LOGICA
                       | STR
                       | ID'''
        if len(p) == 2:
            if p[1][0] == p[1][-1] == '"':
                # Se for string (entre aspas), mantém como string
                p[0] = p[1]
            elif isinstance(p[1], ASTNode):
                p[0] = p[1]
            else:
                # Se for ID, cria ASTNode do tipo ID
                p[0] = ASTNode('ID', value=p[1])

    def p__item_escrita(self, p):
        '''_ITEM_ESCRITA : COMMA ITEM_ESCRITA _ITEM_ESCRITA
                         | '''
        if len(p) == 4:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = []

    def p_condicional(self, p):
        '''CONDICIONAL : SE EXPR_LOGICA ENTAO COMANDOS SENAO COMANDOS FIM
                       | SE EXPR_LOGICA ENTAO COMANDOS FIM'''
        if len(p) == 8:
            p[0] = ASTNode('CONDICIONAL', [p[2], p[4], p[6]], value='SE_SENAO')
        else:
            p[0] = ASTNode('CONDICIONAL', [p[2], p[4]], value='SE')

    def p_repeticao(self, p):
        'REPETICAO : ENQUANTO EXPR_LOGICA FACA COMANDOS FIM'
        p[0] = ASTNode('REPETICAO', [p[2], p[4]])

    def p_expr(self, p):
        'EXPR : TERMO _EXPR'
        p[0] = ASTNode('EXPR', [p[1]] + p[2])

    def p__expr(self, p):
        '''_EXPR : MAIS TERMO _EXPR
                 | MENOS TERMO _EXPR
                 | '''
        if len(p) == 4:
            p[0] = [ASTNode(p[1]), p[2]] + p[3]
        else:
            p[0] = []

    def p_termo(self, p):
        'TERMO : FATOR _TERMO'
        p[0] = ASTNode('TERMO', [p[1]] + p[2])

    def p__termo(self, p):
        '''_TERMO : VEZES FATOR _TERMO
                  | DIV FATOR _TERMO
                  | '''
        if len(p) == 4:
            p[0] = [ASTNode(p[1]), p[2]] + p[3]
        else:
            p[0] = []

    def p_fator(self, p):
        '''FATOR : MENOS FATOR %prec UMINUS
                 | NUM
                 | ID
                 | LPAREN EXPR RPAREN'''
        if len(p) == 3:
            p[0] = ASTNode('UMINUS', [p[2]])
        elif len(p) == 2:
            if isinstance(p[1], int):
                p[0] = ASTNode('NUM', value=p[1])
            else:
                p[0] = ASTNode('ID', value=p[1])
        else:
            p[0] = p[2]

    def p_expr_logica(self, p):
        'EXPR_LOGICA : TERMO_LOGICO _EXPR_LOGICA'
        p[0] = ASTNode('EXPR_LOGICA', [p[1]] + p[2])

    def p__expr_logica(self, p):
        '''_EXPR_LOGICA : OR TERMO_LOGICO _EXPR_LOGICA
                        | '''
        if len(p) == 4:
            p[0] = [ASTNode('OR'), p[2]] + p[3]
        else:
            p[0] = []

    def p_termo_logico(self, p):
        'TERMO_LOGICO : FATOR_LOGICO _TERMO_LOGICO'
        p[0] = ASTNode('TERMO_LOGICO', [p[1]] + p[2])

    def p__termo_logico(self, p):
        '''_TERMO_LOGICO : AND FATOR_LOGICO _TERMO_LOGICO
                         | '''
        if len(p) == 4:
            p[0] = [ASTNode('AND'), p[2]] + p[3]
        else:
            p[0] = []

    def p_fator_logico(self, p):
        '''FATOR_LOGICO : NOT FATOR_LOGICO
                        | RELACIONAL
                        | LPAREN EXPR_LOGICA RPAREN
                        | ID
                        | BOOL'''
        if len(p) == 3:
            p[0] = ASTNode('NOT', [p[2]])
        elif len(p) == 2:
            if isinstance(p[1], ASTNode):
                p[0] = p[1]
            elif isinstance(p[1], bool):
                p[0] = ASTNode('BOOL', value=p[1])
            else:
                p[0] = ASTNode('ID', value=p[1])
        else:
            p[0] = p[2]

    def p_relacional(self, p):
        '''RELACIONAL : EXPR_REL OP_REL EXPR_REL
                      | EXPR OP_INT EXPR'''
        p[0] = ASTNode('RELACIONAL', [p[1], ASTNode(p[2]), p[3]])

    def p_expr_rel(self, p):
        '''EXPR_REL : EXPR
                    | EXPR_LOGICA'''
        p[0] = p[1]

    def p_op_rel(self, p):
        '''OP_REL : IGUAL
                  | DIF'''
        p[0] = p[1]

    def p_op_int(self, p):
        '''OP_INT : MENOR
                  | MENORIG
                  | MAIOR
                  | MAIORIG'''
        p[0] = p[1]

    def p_error(self, p):
        if p:
            raise SyntaxError(f"Erro de syntaxe na linha {getattr(p, 'lineno', '?')}: token '{getattr(p, 'value', '?')}' tipo '{getattr(p, 'type', '?')}'")
        else:
            raise SyntaxError("Erro de syntaxe: final inesperado do arquivo")

# Adaptador para lista de tokens (PLY espera um lexer com método token())
class TokenListLexer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
    def token(self):
        if self.index < len(self.tokens):
            tok = self.tokens[self.index]
            self.index += 1
            return tok
        return None
