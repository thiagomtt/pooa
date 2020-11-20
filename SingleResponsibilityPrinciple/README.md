# Single Responsibility Principle

### O que é?

Single Responsibility Principle (ou Princípio da responsabilidade única) é o 
primeiro item do acrônimo [SOLID](https://medium.com/desenvolvendo-com-paixao/o-que-%C3%A9-solid-o-guia-completo-para-voc%C3%AA-entender-os-5-princ%C3%ADpios-da-poo-2b937b3fc530),
criado por *Michael Feathers*.
O acrônimo foi inspirado nos cinco princípios da orientação a objetos e design de código criados por 
[*Robert C. Martin*](https://en.wikipedia.org/wiki/Robert_C._Martin).

O Princípio da responsabilidade única enuncia que toda classe/função deve ser criada com apenas um 
objetivo dentro do código, ou seja, só existe um motivo para ela ser executada e alterada.

Essa é uma boa prática de programação visto que sua aplicação tem direto impacto na produtividade 
pois se torna mais fácil a divisão de tarefas bem como a resolução de problemas e *bugs* dentro do software, 
por membros de um mesmo time de desenvolvimento.

### Exemplos 

Abaixo temos um exemplo onde a função *lancamento* viola o SRP (Single Responsibility Principle) obervando que ao receber
os dados para realizar um lançamento em uma conta bancária a função realiza as tarefas de:

*	Validar as informações de lançamento
*	Imprime saídas para erros/sucesso da operação
*	Realiza de fato o lançamento no sistema

```c++
void lancamento(int numConta, int operacao, float valor, Data data){
    int i=0; int cont=0; float novoValor=0;

    do{
        if(numConta == id_ContaCorrente[i]->getNumConta())
            cont += 1;
        i += 1;
    }while(i<numContasCadastradas);
    //Não existe esse numero de conta
    if(cont == 0){
        cout << endl << "ERRO! Não há nenhuma conta correspondente com o número inserido" << endl;
        cout << "Você será redirecionado para o menu de lançamentos" << endl;
        menuLancamento();
    }
    //Operação 1 = Débito
    //Operação 2 = Crédito
    if(operacao == 1){
    	// Conta corrente não tem saldo suficiente para débito
        if((id_ContaCorrente[i]->getSaldoAtual() - valor) < 0){
            cout << endl << "ERRO! A conta não tem saldo suficiente para o débito" << endl;
            cout << "Você será redirecionado para o menu de lançamentos" << endl;
            menuLancamento();        	
        }
        else {
        	// Conta corrente tem saldo 
            novoValor = id_ContaCorrente[i]->getSaldoAtual() - valor;
            id_ContaCorrente[i]->setSaldoAtual(novoValor);
            
            Lancamento *lancamento = (Lancamento*) malloc(sizeof(Lancamento));
            lancamento->setLancamento(numConta, operacao, valorLancamento, dataLancamento);
            id_Lancamentos[numLancamentosEfetuados] = lancamento;
            numLancamentosEfetuados += 1;

            cout << endl << "Lançamento realizado com sucesso!" << endl;
            cout << "Você será redirecionado para o menu de lançamentos" << endl;
            menuLancamento();
        }
    }
    else{
    	// Conta recebe o valor indicado, não há restrições para crédito
        novoValor = id_ContaCorrente[i]->getSaldoAtual() + valor;
        id_ContaCorrente[i]->setSaldoAtual(novoValor);

        Lancamento *lancamento = (Lancamento*) malloc(sizeof(Lancamento));
        lancamento->setLancamento(numConta, operacao, valorLancamento, dataLancamento);
        id_Lancamentos[numLancamentosEfetuados] = lancamento;
        numLancamentosEfetuados += 1;

        cout << endl << "Lançamento realizado com sucesso!" << endl;
        cout << "Você será redirecionado para o menu de lançamentos" << endl;
        menuLancamento();        
    }
}
```

Se aplicarmos o SRP na função *lancamento* podemos obter o seguinte código 
agora somente com a responsabilidade de verificar os dados recebidos e direcionar 
para cada ação adequada. 

```c++
void lancamento(int numConta, int operacao, float valor, Data data){
    int i=0; int cont=0; float novoValor=0;

    do{
        if(numConta == id_ContaCorrente[i]->getNumConta())
            cont += 1;
        i += 1;
    }while(i<numContasCadastradas);
    //Não existe esse numero de conta
    if(cont == 0){
    	imprimeResultado(1);
    	menuLancamento();
    }
    //Operação 1 = Débito
    //Operação 2 = Crédito
    if(operacao == 1){
    	// Conta corrente não tem saldo suficiente para débito
        if((id_ContaCorrente[i]->getSaldoAtual() - valor) < 0){
            imprimeResultado(2);
            menuLancamento();        	
        }
        else {
        	// Conta corrente tem saldo 
            efetuaLancamento(1, numConta, operacao, valorLancamento, dataLancamento);
            imprimeResultado(0);
            menuLancamento();
        }
    }
    else{
    	// Conta recebe o valor indicado, não há restrições para crédito
        efetuaLancamento(2, numConta, operacao, valorLancamento, dataLancamento);
        imprimeResultado(0);
        menuLancamento();        
    }
}
```

Da mesma forma agora temos as funções criadas *efetuaLancamento* e *imprimeResultado* 
respeitando o SRP. Como podemos observar:

```c++
void imprimeResultado(int resultado){
	switch(resultado){
		// Sucesso
		case 0:{
        	cout << endl << "Lançamento realizado com sucesso!" << endl;
        	cout << "Você será redirecionado para o menu de lançamentos" << endl;
        	break;
        }
        // A conta não existe 
        case 1:{
        	cout << endl << "ERRO! Não há nenhuma conta correspondente com o número inserido" << endl;
        	cout << "Você será redirecionado para o menu de lançamentos" << endl;
        	break;
        }
        // A conta não tem saldo suficiente
        case 2:{
        	cout << endl << "ERRO! A conta não tem saldo suficiente para o débito" << endl;
            cout << "Você será redirecionado para o menu de lançamentos" << endl;
            break;
        }
        default:
        	break;
	}
}
```

```c++
void efetuaLancamento(int operacao, int numConta, int operacao, float valor, Data data){
	if(operacao == 1){
		novoValor = id_ContaCorrente[i]->getSaldoAtual() - valor;
        id_ContaCorrente[i]->setSaldoAtual(novoValor);
            
        Lancamento *lancamento = (Lancamento*) malloc(sizeof(Lancamento));
        lancamento->setLancamento(numConta, operacao, valorLancamento, dataLancamento);
        id_Lancamentos[numLancamentosEfetuados] = lancamento;
        numLancamentosEfetuados += 1;
	}
	else{
		novoValor = id_ContaCorrente[i]->getSaldoAtual() + valor;
        id_ContaCorrente[i]->setSaldoAtual(novoValor);

        Lancamento *lancamento = (Lancamento*) malloc(sizeof(Lancamento));
        lancamento->setLancamento(numConta, operacao, valorLancamento, dataLancamento);
        id_Lancamentos[numLancamentosEfetuados] = lancamento;
        numLancamentosEfetuados += 1;
	}
}
```

Concluímos com isso que respeitando o SRP obtemos um código mais limpo e consequentemente melhor para realizar manutenções/upgrades se necessário. 


> A função usada como exemplo foi tirada do repositório [poo-trab1](https://github.com/thiagomtt/poo-trab1/tree/master).

> Escrito por Thiago de Moraes Teixeira - 760667
