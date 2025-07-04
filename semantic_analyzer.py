class SemanticNode:
    def __init__(self, type_, children=None, value=None, action=None):
        self.type = type_
        self.children = children if children is not None else []
        self.value = value
        if action is None:
            def action():
                return self.value
            self.action = action
        else:
            self.action = action  # Função a ser executada pelo Executor

    def __repr__(self):
        return f"SemanticNode(type={self.type}, value={self.value}, children={self.children})"

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def analyze(self, ast):
        print('Análise semântica:')
        dependence_tree = self._visit(ast)
        if self.errors:
            for err in self.errors:
                print(f"Erro semântico: {err}")
            return None
        print('Fim da análise semântica.')
        return dependence_tree

    def _visit(self, node):
        # Se node for string ou valor literal, retorna como está
        if isinstance(node, (str, int, bool)):
            return node
        method = getattr(self, f'_visit_{node.type.lower()}', self._visit_generic)
        return method(node)

    def _visit_generic(self, node):
        # Visita recursivamente todos os filhos
        if len(node.children) > 1:
            print('node.type generico')
            print(node.type)
            def action():
                print(f'generic {node.type}')
                res = node.value
                print(f'generic value {res}')
                return res
            return SemanticNode(node.type, [], node.value, action=action)


        if len(node.children) == 0:
            def action():
                res = node.value
                return res
            return SemanticNode(node.type, [], node.value, action=action)

        children = [self._visit(node.children[0])]
        def action():
            res = children[0].action()
            return res
        return SemanticNode(node.type, children, node.value, action=action)

    def _visit_prog(self, node):
        [id_node, declaracoes, composto] = node.children
        children = [self._visit(declaracoes), self._visit(composto)]

        def action():
            children[0].action()
            res = children[1].action()
            return res


        return SemanticNode('PROG', children=children, value=id_node.value, action=action)

    def _visit_declaracoes(self, node):
        [declaracao, _declaracao] = node.children
        children = [self._visit(declaracao), self._visit(_declaracao)]
        def action():
            children[0].action()
            res = children[1].action()
            return res
        return SemanticNode('DECLARACOES', children, action=action)

    def _visit_declaracao(self, node):
        [_, __, tipo] = node.children
        def getIds(node):
            if len(node.children) == 0:
                return
            head = [node.children[0]]
            tail = getIds(node.children[1]) 
            res = head if tail == None else head + tail

            return res

        ids = getIds(node)
        for id_node in ids:

            var = id_node.value
            if var in self.symbol_table:
                self.errors.append(f"Variável '{var}' já declarada.")
            else:
                self.symbol_table[var] = (tipo.value,None)

        def action():
            for id_node in ids:
                var = id_node.value
                if var in self.symbol_table:
                    self.errors.append(f"Variável '{var}' já declarada.")
                else:
                    self.symbol_table[var] = (tipo.value,None)

        return SemanticNode('DECLARACAO', [ids, tipo], action=action)

    def _visit__declaracoes(self, node):
        # Declarações de variáveis
        children = []
        if len(node.children) == 2:
            [declaracao, _declaracao] = node.children
            children = [self._visit(declaracao), self._visit(_declaracao)]

        return SemanticNode('_DECLARACAO', children)

    def _visit_composto(self, node):
        # O nó 'COMPOSTO' possui um filho: 'comandos'
        [comandos] = node.children
        children = [self._visit(comandos)]

        def action():
            def exec_comandos(node):
                if node is not None and len(node.children) == 0:
                    return
                
                res = node.children[0].action()
                res2 = exec_comandos(node.children[1])
                return res if res2 == None else res2

            res = exec_comandos(children[0])
            return res
        return SemanticNode('COMPOSTO', children, action=action)

    def _visit_comandos(self, node):
        [comando, _comando] = node.children
        children = [self._visit(comando), self._visit(_comando)]
        def action():
            res1 = children[0].action()
            res2 = children[1].action()
            return res1 if res2 == None else res2
        return SemanticNode('COMANDOS', children, action=action)
        
    def _visit_comando(self, node):
        [comando] = node.children
        children = [self._visit(comando)]
        def action():
            res = children[0].action()
        return SemanticNode('COMANDO', children, action=action)

    def _visit__comando(self, node):
        children = []
        if len(node.children) == 2:
            [comando, _comando] = node.children
            children = [self._visit(comando), self._visit(_comando)]
        return SemanticNode('_COMANDO', children)

    def _visit_atribuicao(self, node):
        [id_node, expr] = node.children
        var = id_node.value
        children = [self._visit(var), self._visit(expr)]
        if var not in self.symbol_table.keys():
            self.errors.append(f"Variável '{var}' não declarada.")
            table_type = None
        else:
            (table_type, _) = self.symbol_table[var]
        expr_type = 'inteiro' if expr.type == 'EXPR' else 'logico'
        if table_type and expr_type and table_type != expr_type:
            self.errors.append(f"Atribuição incompatível: variável '{var}' é do tipo '{table_type}' mas expressão é do tipo '{expr_type}'.")
        def action():
            value = children[1].action()
            self.symbol_table[var] = (table_type, value)
            return value
        return SemanticNode('ATRIBUICAO', children=children, action=action)

    def _visit_leitura(self, node):

        def getIds(node):
            if len(node.children) == 0:
                return
            head = [node.children[0]]
            tail = getIds(node.children[1]) 
            res = head if tail == None else head + tail

            return res

        ids = getIds(node)
        for id_node in ids:
            var = id_node.value
            if var not in self.symbol_table.keys():
                self.errors.append(f"Variável '{var}' não declarada para leitura.")

        def action():
            for id_node in ids:
                var = id_node.value
                (table_type, _) = self.symbol_table[var]
                read = input()
                if (read == 'verdadeiro' or read == 'falso') and table_type == 'logico':
                    self.symbol_table[var] = (table_type, read)
                else:
                    try:
                        self.symbol_table[var] = (table_type, int(read))
                    except:
                        print(f"Erro semântico: Não foi possivel converter o valor '{read}' para o tipo '{table_type}'.")
                        exit()


        return SemanticNode('LEITURA', ids, action=action)

    def _visit_escrita(self, node):
        expr = node.children[0]
        children = [self._visit(expr)]

        def action():
            print(children[0].action())
        return SemanticNode('ESCRITA', children, action=action)

    def _visit_expr_str(self, node):
        [item, _item] = node.children
        children = [self._visit(item), self._visit(_item)]
        def action():
            val = children[0].action()
            if children[0].type == 'ID':
                (_, val) = self.symbol_table[val]
            items = [val] + children[1].action()
            return ' '.join([ f'{i}' for i in items ])
                

        return SemanticNode('EXPR_STR', children, action=action)
    
    def _visit__item_escrita(self, node):
        if len(node.children) == 0:
            def action():
                return []
            return SemanticNode('_ITEM_ESCRITA', action=action)

        [item, _item] = node.children
        children = [self._visit(item), self._visit(_item)]
        def action():
            val = children[0].action()
            if children[0].type == 'ID':
                (_, val) = self.symbol_table[val]
            items = [val] + children[1].action()
            return items
        
        return SemanticNode('_ITEM_ESCRITA', action=action)
        
    def _visit_condicional(self, node):
        # node.value pode ser 'SE' ou 'SE_SENAO'
        cond = self._visit(node.children[0])
        bloco_se = self._visit(node.children[1])
        if node.value == 'SE_SENAO':
            bloco_senao = self._visit(node.children[2])
            return SemanticNode('CONDICIONAL', [cond, bloco_se, bloco_senao], 'SE_SENAO')
        return SemanticNode('CONDICIONAL', [cond, bloco_se], 'SE')

    def _visit_repeticao(self, node):
        cond = self._visit(node.children[0])
        bloco = self._visit(node.children[1])
        return SemanticNode('REPETICAO', [cond, bloco])

    def _visit_expr(self, node):
        [termo, _expr] = node.children
        children = [self._visit(termo), self._visit(_expr)]

        def action():
            if children[1].value == '+':
                termo = children[0].action() 
                expr = children[1].action()
                return termo + expr
            elif children[1].value == '-':
                termo = children[0].action() 
                expr = children[1].action()
                return termo - expr
            else:
                termo = children[0].action()
                return termo

        return SemanticNode('EXPR', children, action=action)

    def _visit__expr(self, node):
        if len(node.children) == 0:
            def action():
                return 0
            return SemanticNode('_EXPR', [], action=action, value=node.value)
        [termo, _expr] = node.children
        children = [self._visit(termo), self._visit(_expr)]

        def action():
            if _expr.value == '+':
                termo = children[0].action() 
                expr = children[1].action()
                print(termo + expr)
                return termo + expr
            elif _expr.value == '-':
                termo = children[0].action() 
                expr = children[1].action()
                return termo - expr
            else:
                res = children[0].action()
                return res

        return SemanticNode('_EXPR', children, action=action, value=node.value)

    def _visit_expr_logica(self, node):
        [termo, _expr] = node.children
        children = [self._visit(termo), self._visit(_expr)]

        def action():
            if children[1].value == '||':
                termo = children[0].action() 
                expr = children[1].action()
                return termo or expr
            else:
                termo = children[0].action()
                return termo

        return SemanticNode('EXPR_LOGICA', children, action=action)

    def _visit__expr_logica(self, node):
        if len(node.children) == 0:
            def action():
                return 0
            return SemanticNode('_EXPR_LOGICA', [], action=action, value=node.value)
        [termo, _expr] = node.children
        children = [self._visit(termo), self._visit(_expr)]

        def action():
            if _expr.value == '||':
                return children[0].action() or children[1].action()
            else:
                return children[0].action()

        return SemanticNode('_EXPR_LOGICA', children, action=action, value=node.value)

    def _visit_termo_logico(self, node):
        if len(node.children) == 0:
            def action():
                return 1
            return SemanticNode('TERMO_LOGICO', [], action=action, value=node.value)
        [fator, _termo] = node.children
        children = [self._visit(fator), self._visit(_termo)]
        def action():
            if _termo.value == '&&':    
                fator = children[0].action()
                termo = children[1].action()
                res = fator and termo
                return res
            else:
                res = children[0].action()
                return res

        return SemanticNode('TERMO_LOGICO', children, value=node.value, action=action)

    def _visit__termo_logico(self, node):
        if len(node.children) == 0:
            def action():
                return 1
            return SemanticNode('_TERMO_LOGICO', [], action=action, value=node.value)
        [fator, _termo] = node.children
        children = [self._visit(fator), self._visit(_termo)]

        def action():
            if _termo.value == '&&':
                return children[0].action() and children[1].action()
            else:
                return children[0].action()

        return SemanticNode('_TERMO_LOGICO', children, action=action, value=node.value)

    def _visit_fator_logico(self, node):
        children = [self._visit(node.children[0])]
        
        def action():
            if children[0].type == 'ID':
                if children[0].value not in self.symbol_table:
                    self.errors.append(f"Variável '{children[0].value}' não declarada.")
                (_, value) = self.symbol_table[children[0].value]
                return value
            if children[0].type == 'BOOL':
                return children[0].value
            child_res = children[0].action()
            if children[0].type == 'NOT':
                return not child_res

            # FATOR_LOGICO | RELACIONAL
            return child_res
                
            

            
        return SemanticNode('FATOR_LOGICO', children, action=action, value=node.value)

    def _visit_relacional(self, node):
        # falta implementar esta caralha em diante pro tipo logico funcionar
        [expr1, expr2] = node.children
        children = [self._visit(expr1), self._visit(expr2)]

        def action():
            if node.value == '<':
                termo = children[0].action()
                expr = children[1].action()
                return termo < expr
            elif node.value == '<=':
                termo = children[0].action() 
                expr = children[1].action()
                return termo <= expr
            elif node.value == '>':
                termo = children[0].action() 
                expr = children[1].action()
                return termo > expr
            elif node.value == '>=':
                termo = children[0].action() 
                expr = children[1].action()
                return termo >= expr

        return SemanticNode('EXPR', children, action=action)



    def _visit_termo(self, node):
        if len(node.children) == 0:
            def action():
                return 1
            return SemanticNode('TERMO', [], action=action, value=node.value)
        [fator, _termo] = node.children
        children = [self._visit(fator), self._visit(_termo)]
        def action():
            if _termo.value == '*':
                fator = children[0].action()
                termo = children[1].action()
                res = fator * termo
                return res
            elif _termo.value == '/':
                fator = children[0].action()
                termo = children[1].action()
                res = fator / termo
                return res
            else:
                res = children[0].action()
                return res

        return SemanticNode('TERMO', children, value=node.value, action=action)
    
    def _visit__termo(self, node):
        if len(node.children) == 0:
            def action():
                return 1
            return SemanticNode('_TERMO', [], action=action, value=node.value)
        [fator, _termo] = node.children
        children = [self._visit(fator), self._visit(_termo)]

        def action():
            if _termo.value == '*':
                return children[0].action() * children[1].action()
            elif _termo.value == '/':
                return children[0].action() / children[1].action()
            else:
                return children[0].action()

        return SemanticNode('_TERMO', children, action=action, value=node.value)

    def _visit_fator(self, node):
        children = [self._visit(node.children[0])]
        child_type = children[0].type

        if child_type == 'UMINUS':
            def action():
                return -children[0].action()
            return SemanticNode('UMINUS', children, action=action)
        if child_type == 'NUM':
            def action():
                return int(children[0].value)
            return SemanticNode('NUM', action=action)
        if child_type == 'ID':
            if children[0].value not in self.symbol_table:
                self.errors.append(f"Variável '{children[0].value}' não declarada.")
            def action():
                (_, value_int) = self.symbol_table[children[0].value]
                return value_int
            return SemanticNode('ID', value=children[0].value, action=action)
        if child_type == 'BOOL':
            def action():
                return children[0].value
            return SemanticNode('BOOL', action=action)
        # Parênteses ou outros fatores
        children = [self._visit(children[0].children[0])]
        def action():
            return children[0].action()
        return SemanticNode(children[0].type, children, action=action, value=node.value)

    def _visit_uminus(self, node):
        children = [self._visit(node.children[0])]
        def action():
            return children[0].action()
        return SemanticNode('UMINUS', action=action)

    def _visit_op_rel(self, node):
        return SemanticNode('OP_REL', value=node.value)
