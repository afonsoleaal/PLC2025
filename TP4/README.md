# **TPC DA AULA 4**

Afonso Leal,a108472

## TPC4: Máquina de vending

Construir um programa que simule uma máquina de vending.
A máquina tem um stock de produtos: uma lista de triplos, nome do produto, quantidade e preço.

```
stock = [
{"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
...
}
```

Pode-se persistir essa lista num ficheiro em JSON que é carregado no arranque do programa e é atulizado
quando o programa termina.
A seguir apresenta-se um exemplo de uma interação com a máquina, assim que esta é ligada, para que
possas perceber o tipo de comandos que a máquina aceita (as linhas iniciadas marcadas com >>
representam o input do utilizador):

```
maq: 2024-03-08, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
cod | nome | quantidade | preço
---------------------------------
A23 água 0.5L 8 0.7
...
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60c
>> SELECIONAR A23
maq: Saldo insufuciente para satisfazer o seu pedido
maq: Saldo = 60c; Pedido = 70c
>> ...
...
maq: Saldo = 74c
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c e 2x 2c.
maq: Até à próxima
```

O stock encontra-se inicialmente armazenado num ficheiro JSON de nome "stock.json" que é carregado
em memória quando o programa arranca. Quando o programa termina, o stock é gravado no mesmo
ficheiro, mantendo assim o estado da aplicação entre interações.
Use a imaginação e criatividade e tente contemplar todos os cenários, por exemplo, produto inexistente ou
stock vazio.
Como extra pode adicionar um comando para adicionar alguns produtos ao stock existente (produtos
novos ou já existentes).

[Resolução](./tpc4.py)
