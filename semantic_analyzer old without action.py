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
        children = [self._visit(child) if isinstance(child, (SemanticNode, type(node))) else child for child in (node.children if hasattr(node, 'children') else [])]
        def action():
            return node.value
        return SemanticNode(node.type, children, node.value, action)

    def _visit_prog(self, node):
        # Raiz do programa
        children = [self._visit(child) for child in node.children]
        def action():
            print('start program', node)
            result = None
            for child in children:
                if hasattr(child, 'action') and callable(child.action):
                    result = child.action()
            return result
        return SemanticNode('PROG', children, node.value, action)

    def _visit_declaracoes(self, node):
        # Declarações de variáveis
        decls = [self._visit(decl) for decl in node.children]
        def action():
            print('start declaracoes', node)
            for decl in decls:
                if hasattr(decl, 'action') and callable(decl.action):
                    decl.action()
        return SemanticNode('DECLARACOES', decls, action=action)

    def _visit_declaracao(self, node):
        ids, tipo = node.children
        for var in ids:
            if var in self.symbol_table:
                self.errors.append(f"Variável '{var}' já declarada.")
            else:
                self.symbol_table[var] = (tipo.value, None) if hasattr(tipo, 'value') else (tipo, None)
                # self.symbol_table[var] = tipo.value if hasattr(tipo, 'value') else tipo
        def action():
            pass  # Declaração não executa nada em tempo de execução
        return SemanticNode('DECLARACAO', [ids, tipo], action)

    def _visit_atribuicao(self, node):
        var = node.value
        expr = self._visit(node.children[0])
        if var not in self.symbol_table:
            self.errors.append(f"Variável '{var}' não declarada.")
            var_type = None
        else:
            var_type = self.symbol_table[var][0]
        expr_type = 'inteiro' if hasattr(expr, 'type') and expr.type == 'EXPR' else 'logico'
        if var_type and expr_type and var_type != expr_type:
            self.errors.append(f"Atribuição incompatível: variável '{var}' é do tipo '{var_type}' mas expressão é do tipo '{expr_type}'.")
        def action():
            value = expr.action() if hasattr(expr, 'action') and callable(expr.action) else None
            self.symbol_table[var] = (self.symbol_table[var][0], value)
            return value
        return SemanticNode('ATRIBUICAO', [expr], var, action)

    def _visit_leitura(self, node):
        ids = node.children[0] if isinstance(node.children[0], list) else [node.children[0]]
        for var in ids:
            if var not in self.symbol_table:
                self.errors.append(f"Variável '{var}' não declarada para leitura.")
        def action():
            for var in ids:
                self.symbol_table[var] = (self.symbol_table[var][0], input())
        return SemanticNode('LEITURA', ids, action=action)

    def _visit_escrita(self, node):
        exprs = [self._visit(expr) for expr in (node.children[0] if isinstance(node.children[0], list) else [node.children[0]])]

        def action():
            print('start escrita')
            for expr in exprs:
                if hasattr(expr, 'action') and callable(expr.action):
                    value = expr.action()
                elif hasattr(expr, 'value'):
                    value = expr.value
                else:
                    value = expr  # string literal ou valor simples
                print(value, end=' ')
            print('')
        return SemanticNode('ESCRITA', exprs, action=action)

    def _visit_condicional(self, node):
        cond = self._visit(node.children[0])
        bloco_se = self._visit(node.children[1])
        if node.value == 'SE_SENAO':
            bloco_senao = self._visit(node.children[2])
            def action():
                if cond.action():
                    return bloco_se.action()
                else:
                    return bloco_senao.action()
            return SemanticNode('CONDICIONAL', [cond, bloco_se, bloco_senao], 'SE_SENAO', action=action)
        def action():
            if cond.action():
                return bloco_se.action()
        return SemanticNode('CONDICIONAL', [cond, bloco_se], 'SE', action=action)

    def _visit_repeticao(self, node):
        cond = self._visit(node.children[0])
        bloco = self._visit(node.children[1])
        def action():
            while cond.action():
                bloco.action()
        return SemanticNode('REPETICAO', [cond, bloco], action=action)

    def _visit_expr(self, node):
        children = [self._visit(child) for child in node.children]
        def action():
            # Soma de inteiros
            result = 0
            for child in children:
                val = child.action() if hasattr(child, 'action') and callable(child.action) else child.value
                if val is None:
                    val = 0
                result += val
            return result
        return SemanticNode('EXPR', children, action=action)

    def _visit_expr_logica(self, node):
        children = [self._visit(child) for child in node.children]
        def action():
            # Exemplo: AND/OR
            return all(child.action() for child in children)
        return SemanticNode('EXPR_LOGICA', children, action=action)

    def _visit_termo(self, node):
        children = [self._visit(child) for child in node.children]
        def action():
            # Só multiplica se todos forem números
            vals = []
            for child in children:
                val = child.action() if hasattr(child, 'action') and callable(child.action) else child.value
                vals.append(val)
            if any(isinstance(v, str) for v in vals):
                self.errors.append('Multiplicação inválida: termo contém string.')                
                return 1
                
            result = 1
            for v in vals:
                if v is None:
                    v = 1
                result *= v
            return result
        return SemanticNode('TERMO', children, action=action)

    def _visit_fator(self, node):
        if node.type == 'UMINUS':
            child = self._visit(node.children[0])
            def action():
                print('result minus......')
                val = child.action() if hasattr(child, 'action') and callable(child.action) else child.value
                if val is None:
                    val = 0
                print('result minus')
                print(val)
                return -val
            return SemanticNode('UMINUS', [child], action=action)
        if node.type == 'NUM':
            def action():
                val = node.value if node.value is not None else 0
                print('result num')
                print(val)
                return val
            return SemanticNode('NUM', value=node.value, action=action)
        if node.type == 'ID':
            if node.value not in self.symbol_table:
                self.errors.append(f"Variável '{node.value}' não declarada.")
            def action():
                val = self.symbol_table.get(node.value)[1]
                
                if val is None:
                    val = 0
                print('result id')
                print(val)
                return val
            return SemanticNode('ID', value=node.value, action=action)
        if node.type == 'BOOL':
            def action():
                val = node.value if node.value is not None else False
                print('result bool')
                print(val)
                return val
            return SemanticNode('BOOL', value=node.value, action=action)
        children = [self._visit(child) for child in node.children]
        def action():
            val = node.value if node.value is not None else 0
            return val
        return SemanticNode(node.type, children, node.value, action=action)

    def _visit_relacional(self, node):
        children = [self._visit(child) for child in node.children]
        def action():
            # Exemplo: igualdade
            return children[0].action() == children[1].action()
        return SemanticNode('RELACIONAL', children, action=action)

    def _visit_op_rel(self, node):
        def action():
            return node.value
        return SemanticNode('OP_REL', value=node.value, action=action)
