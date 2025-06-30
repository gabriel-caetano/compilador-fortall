import sys
from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer
from executor import Executor

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)
    filename = sys.argv[1]
    lexic = LexicalAnalyzer()
    tokens = lexic.tokenize_file(filename)
    # print(tokens)
    # for token in tokens:
    #     print(token)
    syntax = SyntaxAnalyzer()
    ast = syntax.parse(tokens)
    # print(ast)
    semantic = SemanticAnalyzer()
    dependence_tree = semantic.analyze(ast)
    # # print(dependence_tree)
    # executor = Executor()
    # executor.execute(dependence_tree)
    

if __name__ == "__main__":
    main()

