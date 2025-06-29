class SemanticNode:
    def __init__(self, type_, children=None, value=None):
        self.type = type_
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        return f"SemanticNode(type={self.type}, value={self.value}, children={self.children})"

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def analyze(self, ast):
        """
        Realiza a análise semântica da AST e gera a árvore de execução.
        Retorna a raiz da árvore de execução (SemanticNode) ou None se houver erro.
        """
        print('Análise semântica:')
        exec_tree = self._visit(ast)
        if self.errors:
            for err in self.errors:
                print(f"Erro semântico: {err}")
            return None
        print('Fim da análise semântica.')
        # print(node)
        # print(self.symbol_table)
        return exec_tree

    def _visit(self, node):
        # Se node for string ou valor literal, retorna como está
        if isinstance(node, (str, int, bool)):
            return node
        method = getattr(self, f'_visit_{node.type.lower()}', self._visit_generic)
        return method(node)

    def _visit_generic(self, node):
        # Visita recursivamente todos os filhos
        children = [self._visit(child) if isinstance(child, (SemanticNode, type(node))) else child for child in (node.children if hasattr(node, 'children') else [])]
        return SemanticNode(node.type, children, node.value)

    def _visit_prog(self, node):
        # Raiz do programa
        return SemanticNode('PROG', [self._visit(child) for child in node.children], node.value)

    def _visit_declaracoes(self, node):
        # Declarações de variáveis
        for decl in node.children:
            self._visit(decl)
        return SemanticNode('DECLARACOES', node.children)

    def _visit_declaracao(self, node):
        # node.value = ([id1, id2, ...], tipo)
        ids, tipo = node.children
        for var in ids:
            if var in self.symbol_table:
                self.errors.append(f"Variável '{var}' já declarada.")
            else:
                self.symbol_table[var] = tipo.value if hasattr(tipo, 'value') else tipo
        return SemanticNode('DECLARACAO', [ids, tipo])

    def _visit_atribuicao(self, node):
        var = node.value
        expr = self._visit(node.children[0])
        if var not in self.symbol_table:
            self.errors.append(f"Variável '{var}' não declarada.")
        return SemanticNode('ATRIBUICAO', [expr], var)

    def _visit_leitura(self, node):
        ids = node.children[0] if isinstance(node.children[0], list) else [node.children[0]]
        for var in ids:
            if var not in self.symbol_table:
                self.errors.append(f"Variável '{var}' não declarada para leitura.")
        return SemanticNode('LEITURA', ids)

    def _visit_escrita(self, node):
        # Assume que node.children[0] é uma lista de expressões
        exprs = [self._visit(expr) for expr in (node.children[0] if isinstance(node.children[0], list) else [node.children[0]])]
        return SemanticNode('ESCRITA', exprs)

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
        # Expressão aritmética
        children = [self._visit(child) for child in node.children]
        return SemanticNode('EXPR', children)

    def _visit_expr_logica(self, node):
        # Expressão lógica
        children = [self._visit(child) for child in node.children]
        return SemanticNode('EXPR_LOGICA', children)

    def _visit_termo(self, node):
        children = [self._visit(child) for child in node.children]
        return SemanticNode('TERMO', children)

    def _visit_fator(self, node):
        if node.type == 'UMINUS':
            return SemanticNode('UMINUS', [self._visit(node.children[0])])
        if node.type == 'NUM':
            return SemanticNode('NUM', value=node.value)
        if node.type == 'ID':
            if node.value not in self.symbol_table:
                self.errors.append(f"Variável '{node.value}' não declarada.")
            return SemanticNode('ID', value=node.value)
        if node.type == 'BOOL':
            return SemanticNode('BOOL', value=node.value)
        # Parênteses ou outros fatores
        children = [self._visit(child) for child in node.children]
        return SemanticNode(node.type, children, node.value)

    def _visit_relacional(self, node):
        children = [self._visit(child) for child in node.children]
        return SemanticNode('RELACIONAL', children)

    def _visit_op_rel(self, node):
        return SemanticNode('OP_REL', value=node.value)

    # Adicione outros métodos _visit_* conforme necessário para sua árvore
