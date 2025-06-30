class Executor:
    def execute(self, dependence_tree):
        """
        Percorre a árvore de dependência e executa as ações de cada nó.
        Cada nó deve conter uma função 'action' que será chamada para executar a lógica do nó.
        O valor retornado por cada ação pode ser utilizado conforme a semântica da linguagem.
        """
        return self._execute_node(dependence_tree)

    def _execute_node(self, node):
        # Executa a ação do nó, se existir
        # print(node)?
        result = None
        if hasattr(node, 'action') and callable(node.action):
            result = node.action()
        # Executa recursivamente para os filhos, se existirem
        if hasattr(node, 'children'):
            for child in node.children:
                self._execute_node(child)
        return result
