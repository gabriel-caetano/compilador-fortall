# Lista de tokens compartilhada entre o analisador léxico e sintático
# Todos os nomes de tokens usados na gramática e à implementação

tokens = (
    # Identificadores e literais
    'ID', 'NUM', 'STR', 'BOOL',
    # Palavras reservadas
    'PROGRAMA', 'VAR', 'INTEIRO', 'LOGICO', 'INICIO', 'FIM', 'LER', 'ESCREVER',
    'SENAO', 'ENTAO', 'SE', 'ENQUANTO', 'FACA',
    # Símbolos e operadores
    'SEMI', 'COLON', 'COMMA', 'DOT',
    'MAIS', 'MENOS', 'VEZES', 'DIV',
    'ATRIB', 'IGUAL', 'DIF', 'MENOR', 'MENORIG', 'MAIOR', 'MAIORIG',
    'LPAREN', 'RPAREN',
    # Operadores lógicos
    'OR', 'AND', 'NOT'
)
