/* Exemplo de programa aceito pela gramática */
programa exemplo;
var x, y, z: inteiro;
var a, b: logico;

inicio
    x := 10;
    y := -20;
    z := x + y * (x - 2);
    a := verdadeiro;
    b := falso;
    Ler(x);
    Escrever("Resultado:", z, a, b);
    se x < y entao
        Escrever("x é menor que y");
    se nao
        Escrever("x não é menor que y");
    enquanto z > 0 faca
        z := z - 1;
    inicio
        y := y + 1;
        Escrever("Loop interno", y);
    fim
fim.
/* Fim do programa */
