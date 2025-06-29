/* Exemplo extenso e variado para testes do compilador */
programa exemplo_completo;
var a, b, c, d, e, f, g, h, i, j: inteiro;
var x, y, z: inteiro;
var flag, cond1, cond2, cond3: logico;
var resultado: inteiro;

inicio
    a := 10;
    b := 20;
    c := 30;
    d := 40;
    e := 50;
    f := 60;
    g := 70;
    h := 80;
    i := 90;
    j := 100;
    x := 0;
    y := (j + x);
    z := 2;
    flag := verdadeiro;
    cond1 := falso;
    cond2 := verdadeiro;
    cond3 := falso;
    resultado := 0;

    Escrever("Iniciando o programa de teste completo");
    Escrever("Valores iniciais:", a, b, c, d, e, f, g, h, i, j);
    Escrever("Flags:", flag, cond1, cond2, cond3);

    Ler(a, b, flag);
    Escrever("Valores lidos:", a, b, flag);

    se a > b entao
        Escrever("a maior que b");
        resultado := a - b;
    senao
        Escrever("b maior ou igual a a");
        resultado := b - a;
    fim;

    se (flag && (a < 100)) entao
        Escrever("Flag verdadeiro e a < 100");
    senao
        Escrever("Flag falso ou a >= 100");
    fim;

    enquanto x < 10 faca
        Escrever("Loop externo x:", x);
        y := 0;
        enquanto y < 5 faca
            Escrever("  Loop interno y:", y);
            y := y + 1;
        fim;
        x := x + 1;
    fim;

    i := 5;
    enquanto (i > 0) faca
        Escrever("Contagem regressiva:", i);
        i := i - 1;
    fim;

    se (a = b) || flag entao
        Escrever("a igual a b OU flag verdadeiro");
    senao
        Escrever("a diferente de b E flag falso");
    fim;

    se !cond1 entao
        Escrever("cond1 é falso");
    fim;

    se (a >= 0) && (b <= 100) entao
        Escrever("a está no intervalo válido");
    senao
        Escrever("a fora do intervalo");
    fim;

    resultado := (a + b) * (c - d) / (e + 1);
    Escrever("Resultado de expressão aritmética:", resultado);

    /* Teste de comandos compostos aninhados */
    se (a > 0) entao
        inicio
            Escrever("Entrou no bloco composto");
            se b > 0 entao
                Escrever("b também é positivo");
            senao
                Escrever("b não é positivo");
            fim;
        fim;
    senao
        Escrever("a não é positivo");
    fim;

    /* Teste de múltiplas atribuições e expressões */
    x := 1 + 2 * 3 - 4 / 2;
    y := (x + 5) * (a - 3);
    z := x * y + z - a / b;
    Escrever("x:", x, "y:", y, "z:", z);

    /* Teste de leitura múltipla */
    Ler(c, d, e, cond2);
    Escrever("Valores lidos:", c, d, e, cond2);

    /* Teste de operadores relacionais */
    se a < b entao
        Escrever("a < b");
    fim;
    se a <= b entao
        Escrever("a <= b");
    fim;
    se a > b entao
        Escrever("a > b");
    fim;
    se a >= b entao
        Escrever("a >= b");
    fim;
    se (a = b) entao
        Escrever("a = b");
    fim;
    se a <> b entao
        Escrever("a <> b");
    fim;

    /* Teste de operadores lógicos */
    se cond1 && cond2 entao
        Escrever("cond1 e cond2 verdadeiros");
    senao
        Escrever("cond1 e cond2 não são ambos verdadeiros");
    fim;
    se cond1 || cond2 entao
        Escrever("cond1 ou cond2 verdadeiro");
    senao
        Escrever("cond1 e cond2 ambos falsos");
    fim;
    se !cond3 entao
        Escrever("cond3 é falso");
    fim;

    /* Teste de escrita com string, variáveis e expressões */
    Escrever("Soma de a e b:", a + b);
    Escrever("Expressão lógica:", flag, cond1);
    Escrever("Fim do programa de teste completo");

fim.
