import sys
from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)
    filename = sys.argv[1]
    la = LexicalAnalyzer()
    tokens = la.tokenize_file(filename)
    # print(tokens)
    sa = SyntaxAnalyzer()
    ast = sa.parse(tokens)
    

if __name__ == "__main__":
    main()

