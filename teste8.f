programa condicional_simples;
var n, i, j: inteiro;
var m: logico;
inicio
    i := 1;
    j := 1;
    m := (i - (i / 2) * 2 = 0);
    n := 5;
    Escrever(n);
    Escrever(n > 0);
    se n > 0 entao
        Escrever("n é positivo");
    senao
        Escrever("n é negativo");
    fim;
fim.