import sys
from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)
    filename = sys.argv[1]
    lexic = LexicalAnalyzer()
    tokens = lexic.tokenize_file(filename)
    # print(tokens)
    syntax = SyntaxAnalyzer()
    ast = syntax.parse(tokens)
    semantic = SemanticAnalyzer()
    execTree = semantic.analyze(ast)
    # print(execTree)
    

if __name__ == "__main__":
    main()

