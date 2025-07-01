import ply.yacc as yacc
from tokens import tokens as tk

class ASTNode:
    def __init__(self, type_, children=None, value=None, depth=1):

        self.depth = depth
        self.type = type_
        self.children = children if children is not None else []
        self.childDepth()
        self.value = value
    
    def setDepth(self, d):
        self.depth = d
        self.childDepth()

    def childDepth(self):
        
        for c in self.children:
            c.setDepth(self.depth+1)

    def __repr__(self):
        return f"ASTNode(type={self.type}, value={self.value}) childrens={len(self.children)}"

class SyntaxAnalyzer:
    tokens = tk
    def __init__(self):
         self.parser = yacc.yacc(module=self, start='PROG', debug=False, write_tables=True, outputdir='./')

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
        id_node = ASTNode('ID', value=p[2])
        declaracoes = p[4]
        composto = p[5]
        p[0] = ASTNode('PROG', [id_node, declaracoes, composto])

    def p_declaracoes(self, p):
        '''DECLARACOES : DECLARACAO _DECLARACAO
                      | '''
        if len(p) == 3:
            declaracao = p[1]
            _declaracao = p[2]
            p[0] = ASTNode('DECLARACOES', children=[declaracao, _declaracao])
        else:
            p[0] = ASTNode('DECLARACOES')

    def p_declaracao(self, p):
        'DECLARACAO : VAR ID _ID COLON TIPO SEMI'
        id_node = ASTNode('ID', value=p[2])
        _id = p[3]
        tipo = p[5]
        p[0] = ASTNode('DECLARACAO', children=[id_node, _id, tipo])

    def p__declaracao(self, p):
        '''_DECLARACAO : DECLARACAO _DECLARACAO
                      | '''
        if len(p) == 3:
            declaracao = p[1]
            _declaracao = p[2]
            p[0] = ASTNode('_DECLARACOES', children=[declaracao, _declaracao])
        else:
            p[0] = ASTNode('_DECLARACOES')

    def p_tipo(self, p):
        '''TIPO : INTEIRO
               | LOGICO'''
        p[0] = ASTNode('TIPO', value=p[1])

    def p__id(self, p):
        '''_ID : COMMA ID _ID
               | '''
        if len(p) == 4:
            id_node = ASTNode('ID', value=p[2])
            _id = p[3]
            p[0] = ASTNode('_ID', children=[id_node, _id])
        else:
            p[0] = ASTNode('_ID')

    def p_composto(self, p):
        'COMPOSTO : INICIO COMANDOS FIM'
        comandos = p[2]
        p[0] = ASTNode('COMPOSTO', children=[comandos])

    def p_comandos(self, p):
        '''COMANDOS : COMANDO SEMI _COMANDO
                    | '''
        if len(p) == 4:
            comando = p[1]
            _comando = p[3]
            p[0] = ASTNode('COMANDOS', children=[comando, _comando])
        else:
            p[0] = ASTNode('COMANDOS')

    def p__comando(self, p):
        '''_COMANDO : COMANDO SEMI _COMANDO
                    | '''
        if len(p) == 4:
            comando = p[1]
            _comando = p[3]
            p[0] = ASTNode('_COMANDO', children=[comando, _comando])
        else:
            p[0] = ASTNode('_COMANDO')

    def p_comando(self, p):
        '''COMANDO : ATRIBUICAO
                   | LEITURA
                   | ESCRITA
                   | COMPOSTO
                   | CONDICIONAL
                   | REPETICAO'''
        p[0] = ASTNode('COMANDO', children=[p[1]])

    def p_atribuicao(self, p):
        '''ATRIBUICAO : ID ATRIB EXPR
                    | ID ATRIB EXPR_LOGICA'''
        id_node = ASTNode('ID', value=p[1])
        expr = p[3]
        p[0] = ASTNode('ATRIBUICAO', children=[id_node, expr])

    def p_leitura(self, p):
        'LEITURA : LER LPAREN ID _ID RPAREN'
        id_node = ASTNode('ID', value=p[3])
        _id = p[4]
        p[0] = ASTNode('LEITURA', children=[id_node, _id])

    def p_escrita(self, p):
        'ESCRITA : ESCREVER LPAREN EXPR_STR RPAREN'
        expr_str = p[3]
        p[0] = ASTNode('ESCRITA', children=[expr_str])

    def p_expr_str(self, p):
        '''EXPR_STR : ITEM_ESCRITA _ITEM_ESCRITA
                    | '''
        if len(p) == 3:
            item_escrita = p[1]
            _item_escrita = p[2]
            p[0] = ASTNode('EXPR_STR', children=[item_escrita, _item_escrita])
        else:
            p[0] = ASTNode('EXPR_STR')

    def p_item_escrita(self, p):
        '''ITEM_ESCRITA : EXPR
                       | EXPR_LOGICA
                       | STR
                       | ID'''
        if isinstance(p[1], ASTNode):
            p[0] = p[1]
        elif p[1][0] == p[1][-1] == '"':
            p[0] = ASTNode('STR', value=p[1])
        else: 
            p[0] = ASTNode('ID', value=p[1])

    def p__item_escrita(self, p):
        '''_ITEM_ESCRITA : COMMA ITEM_ESCRITA _ITEM_ESCRITA
                         | '''
        if len(p) == 4:
            item_escrita = p[2]
            _item_escrita = p[3]
            p[0] = ASTNode('_ITEM_ESCRITA', children=[item_escrita, _item_escrita])
        else:
            p[0] = ASTNode('_ITEM_ESCRITA')

    def p_condicional(self, p):
        '''CONDICIONAL : SE EXPR_LOGICA ENTAO COMANDOS SENAO COMANDOS FIM
                       | SE EXPR_LOGICA ENTAO COMANDOS FIM'''
        expr_logica = p[2]
        comandos_se = p[4]
        if len(p) == 8:
            comandos_senao = p[6]
            p[0] = ASTNode('CONDICIONAL', [expr_logica, comandos_se, comandos_senao], value='SE_SENAO')
        else:
            p[0] = ASTNode('CONDICIONAL', [expr_logica, comandos_se], value='SE')

    def p_repeticao(self, p):
        'REPETICAO : ENQUANTO EXPR_LOGICA FACA COMANDOS FIM'
        expr_logica = p[2]
        comandos = p[4]
        p[0] = ASTNode('REPETICAO', children=[expr_logica, comandos])

    def p_expr(self, p):
        'EXPR : TERMO _EXPR'
        termo = p[1]
        _expr = p[2]
        p[0] = ASTNode('EXPR', children=[termo, _expr])

    def p__expr(self, p):
        '''_EXPR : MAIS TERMO _EXPR
                 | MENOS TERMO _EXPR
                 | '''
        if len(p) == 4:
            operador = p[1]
            termo = p[2]
            _expr = p[3]
            p[0] = ASTNode('_EXPR', [termo, _expr], value=operador)
        else:
            p[0] = ASTNode('_EXPR')

    def p_termo(self, p):
        'TERMO : FATOR _TERMO'
        fator = p[1]
        _termo = p[2]
        p[0] = ASTNode('TERMO', [fator, _termo])

    def p__termo(self, p):
        '''_TERMO : VEZES FATOR _TERMO
                  | DIV FATOR _TERMO
                  | '''
        if len(p) == 4:
            operador = p[1]
            fator = p[2]
            _termo = p[3]
            p[0] = ASTNode('_TERMO', children=[fator, _termo], value=operador)
        else:
            p[0] = ASTNode('_TERMO')

    def p_fator(self, p):
        '''FATOR : MENOS FATOR %prec UMINUS
                 | NUM
                 | ID
                 | LPAREN EXPR RPAREN'''
        if len(p) == 3:
            fator = p[2]
            minus = ASTNode('UMINUS', children=[fator])
            p[0] = ASTNode('FATOR', children=[minus])

        elif len(p) == 2:
            if isinstance(p[1], int):
                num = ASTNode('NUM', value=p[1])
                p[0] = ASTNode('FATOR', children=[num])
            else:
                id_node = ASTNode('ID', value=p[1])
                p[0] = ASTNode('FATOR', children=[id_node])
        else:
            expr = p[2]
            p[0] = ASTNode('FATOR', children=[expr])

    def p_expr_logica(self, p):
        'EXPR_LOGICA : TERMO_LOGICO _EXPR_LOGICA'
        termo_logico = p[1]
        _expr_logica = p[2]
        p[0] = ASTNode('EXPR_LOGICA', [termo_logico, _expr_logica])

    def p__expr_logica(self, p):
        '''_EXPR_LOGICA : OR TERMO_LOGICO _EXPR_LOGICA
                        | '''
        if len(p) == 4:
            operador = p[1]
            termo_logico = p[2]
            _expr_logica = p[3]
            p[0] = ASTNode('_EXPR_LOGICA', children=[termo_logico, _expr_logica], value=operador)
        else:
            p[0] = ASTNode('_EXPR_LOGICA')

    def p_termo_logico(self, p):
        'TERMO_LOGICO : FATOR_LOGICO _TERMO_LOGICO'
        fator_logico = p[1]
        _termo_logico = p[2]
        p[0] = ASTNode('TERMO_LOGICO', children=[fator_logico, _termo_logico])

    def p__termo_logico(self, p):
        '''_TERMO_LOGICO : AND FATOR_LOGICO _TERMO_LOGICO
                         | '''
        if len(p) == 4:
            operador = p[1]
            fator_logico = p[2]
            _termo_logico = p[3]
            p[0] = ASTNode('_TERMO_LOGICO', children=[fator_logico, _termo_logico], value=operador)
        else:
            p[0] = ASTNode('_TERMO_LOGICO')

    def p_fator_logico(self, p):
        '''FATOR_LOGICO : NOT FATOR_LOGICO
                        | RELACIONAL
                        | LPAREN EXPR_LOGICA RPAREN
                        | ID
                        | BOOL'''
        if len(p) == 4:
            # lparen expr_logica rparen
            p[0] = p[2]
        
        elif len(p) == 3:
            # not
            fator_logico = p[2]
            p[0] = ASTNode('NOT', children=[fator_logico])
        else :
            if isinstance(p[1], ASTNode):
                p[0] = p[1]
            elif isinstance(p[1], bool):
                p[0] = ASTNode('BOOL', value=p[1])
            else:
                p[0] = ASTNode('ID', value=p[1])

    def p_relacional(self, p):
        '''RELACIONAL : EXPR_REL OP_REL EXPR_REL
                      | EXPR OP_INT EXPR'''
        operador = p[2]
        expr_l = p[1]
        expr_r = p[3]
        p[0] = ASTNode('RELACIONAL', children=[expr_l, expr_r], value=operador)

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
