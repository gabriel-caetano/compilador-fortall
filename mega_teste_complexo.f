/* Mega Exemplo de programa complexo para teste da gramática */
programa mega_teste_complexo;
var i, j, k, l, m, n, x, y, z, soma, produto, maior, menor, cont, total, idx, idy, idz: inteiro;
var flag, terminou, achou, cond1, cond2, cond3, cond4, cond5: logico;
var nome, status: inteiro;
var resultado: inteiro;
inicio
    Escrever("Início do mega teste complexo");
    soma := 0;
    produto := 1;
    maior := -9999;
    menor := 9999;
    cont := 0;
    total := 0;
    flag := falso;
    terminou := falso;
    achou := falso;
    nome := 0;
    status := 0;
    resultado := 0;
    
    // Inicialização de variáveis
    para i := 1 até 10 faca
        para j := 1 até 10 faca
            x := i * j;
            y := i + j;
            z := i - j;
            soma := soma + x + y + z;
            produto := produto * (x + 1);
            se x > maior entao
                maior := x;
            fim;
            se y < menor entao
                menor := y;
            fim;
            cont := cont + 1;
        fim;
    fim;
    Escrever("Soma:", soma, "Produto:", produto, "Maior:", maior, "Menor:", menor, "Cont:", cont);
    
    // Laço principal com condições aninhadas
    i := 1;
    enquanto i <= 20 faca
        j := 1;
        enquanto j <= 10 faca
            k := 1;
            enquanto k <= 5 faca
                cond1 := (i % 2 = 0) && (j % 3 = 0);
                cond2 := (k > 2) || (i < 10);
                cond3 := !flag && (soma > 1000);
                se cond1 entao
                    Escrever("i:", i, "j:", j, "k:", k, "cond1 verdadeiro");
                    soma := soma + i * j * k;
                senao
                    Escrever("i:", i, "j:", j, "k:", k, "cond1 falso");
                fim;
                se cond2 entao
                    produto := produto + k * j;
                senao
                    produto := produto - k * i;
                fim;
                se cond3 entao
                    flag := verdadeiro;
                fim;
                k := k + 1;
            fim;
            j := j + 1;
        fim;
        i := i + 1;
    fim;
    Escrever("Após laços aninhados: soma=", soma, "produto=", produto, "flag=", flag);
    
    // Teste de busca e contagem
    achou := falso;
    para l := 1 até 50 faca
        se (l * 3) % 7 = 0 entao
            achou := verdadeiro;
            Escrever("Achou múltiplo de 7:", l * 3);
        senao
            Escrever("Não achou em l=", l);
        fim;
        total := total + l;
    fim;
    Escrever("Total após busca:", total, "Achou:", achou);
    
    // Condições aninhadas e flags
    cond4 := (maior > 100) && (menor < 0);
    cond5 := (produto <> 0) || (soma < 0);
    se cond4 entao
        Escrever("Condição 4 verdadeira");
        se cond5 entao
            Escrever("Condição 5 também verdadeira");
        senao
            Escrever("Condição 5 falsa");
        fim;
    senao
        Escrever("Condição 4 falsa");
    fim;
    
    // Simulação de matriz 10x10
    para idx := 1 até 10 faca
        para idy := 1 até 10 faca
            resultado := idx * idy;
            se resultado % 2 = 0 entao
                Escrever("Matriz[", idx, ",", idy, "] = ", resultado, "(par)");
            senao
                Escrever("Matriz[", idx, ",", idy, "] = ", resultado, "(ímpar)");
            fim;
        fim;
    fim;
    
    // Laço de decremento
    n := 100;
    enquanto n > 0 faca
        se n % 10 = 0 entao
            Escrever("n é múltiplo de 10:", n);
        fim;
        n := n - 1;
    fim;
    
    // Teste de leitura e escrita
    Escrever("Digite um valor para x:");
    Ler(x);
    Escrever("Digite um valor para y:");
    Ler(y);
    Escrever("x + y =", x + y);
    
    // Teste de lógica booleana
    flag := (x > y) && (soma > 0);
    se flag entao
        Escrever("Flag verdadeiro");
    senao
        Escrever("Flag falso");
    fim;
    
    // Laço com break simulado
    m := 1;
    terminou := falso;
    enquanto !terminou faca
        Escrever("m:", m);
        se m > 50 entao
            terminou := verdadeiro;
        fim;
        m := m + 1;
    fim;
    
    // Teste de strings e múltiplos tipos
    Escrever("Teste de múltiplos tipos:", "string", 123, x, verdadeiro, falso, flag);
    
    // Laço final para garantir 200 linhas
    para l := 1 até 30 faca
        Escrever("Linha extra:", l);
    fim;
    Escrever("Mega teste finalizado!");
fim.
/* Fim do mega programa de teste */
