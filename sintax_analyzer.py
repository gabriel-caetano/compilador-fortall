import ply.yacc as yacc
from tokens import tokens as tk

class ASTNode:
    def __init__(self, type_, children=None, value=None):
        self.type = type_
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        return f"ASTNode(type={self.type}, value={self.value})\nchildren=[\n{self.children}\n]"

class SintaxAnalyzer:
    tokens = tk
    def __init__(self):
         self.parser = yacc.yacc(module=self, start='PROG', debug=False, write_tables=False)

    def parse(self, tokens):
        return self.parser.parse(lexer=TokenListLexer(tokens))

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

    # Regras sintáticas (adaptadas de sintax.py)
    def p_prog(self, p):
        'PROG : PROGRAMA ID SEMI DECLARACOES INICIO COMANDOS FIM DOT'
        p[0] = ASTNode('PROG', [p[4], p[6]], value=p[2])

    def p_declaracoes_var(self, p):
        'DECLARACOES : VAR IDS COLON TIPO SEMI DECLARACOES'
        p[0] = ASTNode('DECLARACOES', [p[2], p[4], p[6]])

    def p_declaracoes_epsilon(self, p):
        'DECLARACOES : '
        p[0] = ASTNode('DECLARACOES')

    def p_tipo_inteiro(self, p):
        'TIPO : INTEIRO'
        p[0] = ASTNode('TIPO', value='INTEIRO')

    def p_tipo_logico(self, p):
        'TIPO : LOGICO'
        p[0] = ASTNode('TIPO', value='LOGICO')

    def p_comandos(self, p):
        'COMANDOS : COMANDO SEMI COMANDOS'
        p[0] = ASTNode('COMANDOS', [p[1], p[3]])

    def p_comandos_epsilon(self, p):
        'COMANDOS : '
        p[0] = ASTNode('COMANDOS')

    def p_comando(self, p):
        '''COMANDO : ATRIBUICOES
                   | LEITURA
                   | ESCRITA
                   | COMPOSTO
                   | CONDICIONAL
                   | REPETICAO'''
        p[0] = p[1]

    def p_atribuicoes(self, p):
        'ATRIBUICOES : ID ATRIB EXPR'
        p[0] = ASTNode('ATRIBUICAO', [p[3]], value=p[1])

    def p_leitura(self, p):
        'LEITURA : LER LPAREN IDS RPAREN'
        p[0] = ASTNode('LEITURA', [p[3]])

    def p_escrita(self, p):
        'ESCRITA : ESCREVER LPAREN ESPR_STR RPAREN'
        p[0] = ASTNode('ESCRITA', [p[3]])

    def p_espr_str(self, p):
        'ESPR_STR : ITEM_ESCRITA ESPR_STR_'
        p[0] = ASTNode('ESPR_STR', [p[1]] + (p[2].children if p[2] else []))

    def p_espr_str_(self, p):
        'ESPR_STR_ : COMMA ITEM_ESCRITA ESPR_STR_'
        p[0] = ASTNode('ESPR_STR_', [p[2]] + (p[3].children if p[3] else []))

    def p_espr_str_epsilon(self, p):
        'ESPR_STR_ : '
        p[0] = ASTNode('ESPR_STR_')

    def p_item_escrita(self, p):
        '''ITEM_ESCRITA : EXPR
                       | EXPR_LOGICA
                       | STR
                       | ID'''
        p[0] = ASTNode('ITEM_ESCRITA', [p[1]])

    def p_composto(self, p):
        'COMPOSTO : INICIO COMANDOS FIM'
        p[0] = ASTNode('COMPOSTO', [p[2]])

    def p_condicional_se_senao(self, p):
        'CONDICIONAL : SE EXPR_LOGICA ENTAO COMANDOS SENAO COMANDOS FIM'
        p[0] = ASTNode('CONDICIONAL', [p[2], p[4], p[6]], value='SE_SENAO')

    def p_condicional_se(self, p):
        'CONDICIONAL : SE EXPR_LOGICA ENTAO COMANDOS FIM'
        p[0] = ASTNode('CONDICIONAL', [p[2], p[4]], value='SE')

    def p_repeticao(self, p):
        'REPETICAO : ENQUANTO EXPR_LOGICA FACA COMANDOS FIM'
        p[0] = ASTNode('REPETICAO', [p[2], p[4]])

    def p_ids(self, p):
        'IDS : ID _IDS'
        ids = [p[1]]
        if p[2]:
            ids += p[2]
        p[0] = ids

    def p__ids(self, p):
        '_IDS : COMMA ID _IDS'
        ids = [p[2]]
        if p[3]:
            ids += p[3]
        p[0] = ids

    def p__ids_epsilon(self, p):
        '_IDS : '
        p[0] = []

    def p_expr(self, p):
        'EXPR : TERMO EXPR_'
        p[0] = ASTNode('EXPR', [p[1]] + (p[2].children if p[2] else []))

    def p_expr_(self, p):
        '''EXPR_ : MAIS TERMO EXPR_
                 | MENOS TERMO EXPR_
                 | '''
        if len(p) > 1:
            p[0] = ASTNode('EXPR_', [ASTNode(p[1]), p[2]] + (p[3].children if p[3] else []))
        else:
            p[0] = None

    def p_termo(self, p):
        'TERMO : FATOR TERMO_'
        p[0] = ASTNode('TERMO', [p[1]] + (p[2].children if p[2] else []))

    def p_termo_(self, p):
        '''TERMO_ : VEZES FATOR TERMO_
                  | DIV FATOR TERMO_
                  | '''
        if len(p) > 1:
            p[0] = ASTNode('TERMO_', [ASTNode(p[1]), p[2]] + (p[3].children if p[3] else []))
        else:
            p[0] = None

    def p_fator_num(self, p):
        'FATOR : NUM'
        p[0] = ASTNode('NUM', value=p[1])

    def p_fator_id(self, p):
        'FATOR : ID'
        p[0] = ASTNode('ID', value=p[1])

    def p_fator_group(self, p):
        'FATOR : LPAREN EXPR RPAREN'
        p[0] = p[2]

    def p_fator_uminus(self, p):
        'FATOR : MENOS FATOR %prec UMINUS'
        p[0] = ASTNode('UMINUS', [p[2]])

    def p_fator_comma(self, p):
        'FATOR : COMMA FATOR'
        p[0] = ASTNode('COMMA', [p[2]])

    def p_fator_bool(self, p):
        'FATOR : BOOL'
        p[0] = ASTNode('BOOL', value=p[1])

    def p_expr_logica(self, p):
        '''EXPR_LOGICA : TERMO_LOGICO OR EXPR_LOGICA
                      | TERMO_LOGICO'''
        if len(p) == 4:
            p[0] = ASTNode('OR', [p[1], p[3]])
        else:
            p[0] = p[1]

    def p_termo_logico(self, p):
        '''TERMO_LOGICO : FATOR_LOGICO AND TERMO_LOGICO
                        | FATOR_LOGICO'''
        if len(p) == 4:
            p[0] = ASTNode('AND', [p[1], p[3]])
        else:
            p[0] = p[1]

    def p_fator_logico_not(self, p):
        'FATOR_LOGICO : NOT FATOR_LOGICO'
        p[0] = ASTNode('NOT', [p[2]])

    def p_fator_logico_relacional(self, p):
        'FATOR_LOGICO : RELACIONAL'
        p[0] = p[1]

    def p_fator_logico_group(self, p):
        'FATOR_LOGICO : LPAREN EXPR_LOGICA RPAREN'
        p[0] = p[2]

    def p_fator_logico_id(self, p):
        'FATOR_LOGICO : ID'
        p[0] = ASTNode('ID', value=p[1])

    def p_fator_logico_bool(self, p):
        'FATOR_LOGICO : BOOL'
        p[0] = ASTNode('BOOL', value=p[1])

    def p_relacional(self, p):
        'RELACIONAL : EXPR OP_REL EXPR'
        p[0] = ASTNode('RELACIONAL', [p[1], ASTNode(p[2]), p[3]])

    def p_op_rel(self, p):
        '''OP_REL : MENOR
                  | MENORIG
                  | MAIOR
                  | MAIORIG
                  | IGUAL
                  | DIF'''
        p[0] = p[1]

    def p_error(self, p):
        if p:
            raise SyntaxError(f"Erro de sintaxe na linha {getattr(p, 'lineno', '?')}: token '{getattr(p, 'value', '?')}' tipo '{getattr(p, 'type', '?')}'")
        else:
            raise SyntaxError("Erro de sintaxe: final inesperado do arquivo")

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
