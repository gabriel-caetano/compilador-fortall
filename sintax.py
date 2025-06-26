import ply.yacc as yacc
from lex import tokens

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

# Regras sintáticas baseadas na gramatica.txt

def p_prog(p):
    'PROG : PROGRAMA ID SEMI DECLARACOES INICIO COMANDOS FIM DOT'
    pass

def p_declaracoes_var(p):
    'DECLARACOES : VAR IDS COLON TIPO SEMI DECLARACOES'
    pass

def p_declaracoes_epsilon(p):
    'DECLARACOES : '
    pass

def p_tipo_inteiro(p):
    'TIPO : INTEIRO'
    pass

def p_tipo_logico(p):
    'TIPO : LOGICO'
    pass

def p_comandos(p):
    'COMANDOS : COMANDO SEMI COMANDOS'
    pass

def p_comandos_epsilon(p):
    'COMANDOS : '
    pass

def p_comando(p):
    '''COMANDO : ATRIBUICOES
               | LEITURA
               | ESCRITA
               | COMPOSTO
               | CONDICIONAL
               | REPETICAO'''
    pass

def p_atribuicoes(p):
    'ATRIBUICOES : ID ATRIB EXPR'
    pass

def p_leitura(p):
    'LEITURA : LER LPAREN IDS RPAREN'
    pass

def p_escrita(p):
    'ESCRITA : ESCREVER LPAREN ESPR_STR RPAREN'
    pass

def p_espr_str(p):
    'ESPR_STR : ITEM_ESCRITA ESPR_STR_'
    pass

def p_espr_str_(p):
    'ESPR_STR_ : COMMA ITEM_ESCRITA ESPR_STR_'
    pass

def p_espr_str_epsilon(p):
    'ESPR_STR_ : '
    pass

def p_item_escrita(p):
    '''ITEM_ESCRITA : EXPR
                   | EXPR_LOGICA
                   | STR
                   | ID'''
    pass

def p_composto(p):
    'COMPOSTO : INICIO COMANDOS FIM'
    pass

def p_condicional_se_senao(p):
    'CONDICIONAL : SE EXPR_LOGICA ENTAO COMANDOS SENAO COMANDOS FIM'
    pass

def p_condicional_se(p):
    'CONDICIONAL : SE EXPR_LOGICA ENTAO COMANDOS FIM'
    pass

def p_repeticao(p):
    'REPETICAO : ENQUANTO EXPR_LOGICA FACA COMANDOS FIM'
    pass

def p_ids(p):
    'IDS : ID _IDS'
    pass

def p__ids(p):
    '_IDS : COMMA ID _IDS'
    pass

def p__ids_epsilon(p):
    '_IDS : '
    pass

def p_expr(p):
    'EXPR : TERMO EXPR_'
    pass

def p_expr_(p):
    '''EXPR_ : MAIS TERMO EXPR_
             | MENOS TERMO EXPR_
             | '''
    pass

def p_termo(p):
    'TERMO : FATOR TERMO_'
    pass

def p_termo_(p):
    '''TERMO_ : VEZES FATOR TERMO_
              | DIV FATOR TERMO_
              | '''
    pass

def p_fator_num(p):
    'FATOR : NUM'
    pass

def p_fator_id(p):
    'FATOR : ID'
    pass

def p_fator_group(p):
    'FATOR : LPAREN EXPR RPAREN'
    pass

def p_fator_uminus(p):
    'FATOR : MENOS FATOR %prec UMINUS'
    pass

def p_fator_comma(p):
    'FATOR : COMMA FATOR'
    pass

def p_fator_bool(p):
    'FATOR : BOOL'
    pass

def p_expr_logica(p):
    '''EXPR_LOGICA : TERMO_LOGICO OR EXPR_LOGICA
                  | TERMO_LOGICO'''
    pass

def p_termo_logico(p):
    '''TERMO_LOGICO : FATOR_LOGICO AND TERMO_LOGICO
                    | FATOR_LOGICO'''
    pass

def p_fator_logico_not(p):
    'FATOR_LOGICO : NOT FATOR_LOGICO'
    pass

def p_fator_logico_relacional(p):
    'FATOR_LOGICO : RELACIONAL'
    pass

def p_fator_logico_group(p):
    'FATOR_LOGICO : LPAREN EXPR_LOGICA RPAREN'
    pass

def p_fator_logico_id(p):
    'FATOR_LOGICO : ID'
    pass

def p_fator_logico_bool(p):
    'FATOR_LOGICO : BOOL'
    pass

def p_relacional(p):
    'RELACIONAL : EXPR OP_REL EXPR'
    pass

def p_op_rel(p):
    '''OP_REL : MENOR
              | MENORIG
              | MAIOR
              | MAIORIG
              | IGUAL
              | DIF'''
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}: token '{p.value}' tipo '{p.type}'")
    else:
        print("Erro de sintaxe: final inesperado do arquivo")

def parse(input_tokens):
    parser = yacc.yacc()
    return parser.parse(input_tokens)
