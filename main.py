import sys
from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)
    filename = sys.argv[1]
    # lexic analyze 
    lexic = LexicalAnalyzer()
    tokens = lexic.tokenize_file(filename)
    # print tokens
    # for token in tokens:
    #     print(token)
    # syntax analyze
    syntax = SyntaxAnalyzer()
    ast = syntax.parse(tokens)
    # print AST
    # node = ast
    # queue = [node]
    # while len(queue) > 0:
    #     print(f"{'-|'*queue[0].depth}: {queue[0]}")
    #     if queue[0].children:
    #         queue = queue[0].children + queue[1:]
    #     else:
    #         queue = queue[1:]
    # semantic analyze
    semantic = SemanticAnalyzer()
    dependence_tree = semantic.analyze(ast)
    # execute
    dependence_tree.action()

if __name__ == "__main__":
    main()

