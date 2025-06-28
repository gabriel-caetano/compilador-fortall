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
        inicio
            y := y + 1;
            Escrever("Loop interno", y);
        fim;
    senao
        Escrever("x não é menor que y");
    fim;
    enquanto z > 0 faca
        z := z - 1;
    fim;
fim.
/* Fim do programa */
