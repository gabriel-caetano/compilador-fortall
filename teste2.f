/* Exemplo válido 2 - teste complexo */
programa teste_logico_completo;
var x, y, z, total: inteiro;
var flag, cond, terminou: logico;
inicio
    x := 7;
    y := -3;
    z := 0;
    total := 0;
    flag := falso;
    terminou := falso;
    Escrever("Início do teste lógico completo");
    Ler(x);
    Ler(y);
    z := 1;
    enquanto z <= 5 faca
        total := total + x * z - y / (z + 1);
        Escrever("z:", z, "total:", total);
        cond := (total > 10) && (z <> 3);
        se cond entao
            Escrever("Condição verdadeira para z:", z);
        senao
            Escrever("Condição falsa para z:", z);
        fim;
        z := z + 1;
    fim;
    flag := (x < y) || (total >= 0);
    se !flag entao
        Escrever("Flag é falso");
    senao
        Escrever("Flag é verdadeiro");
    fim;
    enquanto !terminou faca
        Escrever("Loop até total < 0");
        total := total - 5;
        se total < 0 entao
            terminou := verdadeiro;
            Escrever("Finalizando loop");
        fim;
    fim;
    Escrever("Fim do teste", x, y, z, total, flag, cond, terminou);
fim.
