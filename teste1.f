/* Exemplo complexo para teste completo da gramática */
programa teste_completo;
var a, b, c, i, j, resultado, temp: inteiro;
var flag, cond1, cond2, terminou: logico;
inicio
    a := 10;
    b := 20;
    c := -5;
    resultado := 0;
    flag := falso;
    terminou := falso;
    Escrever("Início do programa de teste completo");
    Ler(a);
    Ler(b);
    Ler(c);
    i := 1;
    enquanto i <= 3 faca
        Escrever("Iteração externa:", i);
        j := 1;
        enquanto j <= 2 faca
            temp := (a + b) * (c - i) / (j + 1);
            Escrever("i:", i, "j:", j, "temp:", temp);
            se temp < 0 entao
                Escrever("temp negativo");
            senao
                Escrever("temp positivo ou zero");
            fim;
            resultado := resultado + temp;
            j := j + 1;
        fim;
        i := i + 1;
    fim;
    cond1 := (a > b) || (c < 0);
    cond2 := !flag && (resultado <> 0);
    se cond1 entao
        Escrever("cond1 verdadeiro");
    senao
        Escrever("cond1 falso");
    fim;
    se cond2 entao
        Escrever("cond2 verdadeiro");
    senao
        Escrever("cond2 falso");
    fim;
    enquanto !terminou faca
        Escrever("Loop principal");
        resultado := resultado - 1;
        se resultado <= 0 entao
            terminou := verdadeiro;
            Escrever("Finalizando loop principal");
        fim;
    fim;
    Escrever("Expressões lógicas:", cond1, cond2, flag, terminou);
    Escrever("Expressões aritméticas:", a, b, c, resultado, temp);
    Escrever("Testando string, número, id e bool", "string", 123, a, verdadeiro);
fim.