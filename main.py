import sys
from lexical_analyzer import LexicalAnalyzer
from sintax_analyzer import SintaxAnalyzer

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)
    filename = sys.argv[1]
    la = LexicalAnalyzer()
    tokens = la.tokenize_file(filename)
    print("\nAnálise semântica:")
    sa = SintaxAnalyzer()
    ast = sa.parse(tokens)
    print("Análise semântica concluída.")
    

if __name__ == "__main__":
    main()

