import sys
from lex import tokenize
from sintax import parse

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    tokens = tokenize(code)
    print("Tokens gerados:")
    print(tokens)
    print("\nAnálise sintática:")
    parse(code)
    print("Análise sintática concluída.")
    

if __name__ == "__main__":
    main()

