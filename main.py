import sys
from lex import tokenize

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    tokens = tokenize(code)
    print(tokens)

if __name__ == "__main__":
    main()

