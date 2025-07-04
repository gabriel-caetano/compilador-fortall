programa aninhamento;
var x, y: inteiro;
inicio
    x := 5;
    y := 3;
    Escrever(x <> 5);
    se x < y entao
        se y < 10 entao
            Escrever("y menor que 10");
        fim;
    senao
        Escrever("x não é menor que y");
    fim;
fim.