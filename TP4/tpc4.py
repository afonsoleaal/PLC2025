import json
import datetime
import sys

# Nome do ficheiro para persistir o stock
NOME_FICHEIRO_STOCK = "stock.json"

def carregar_stock(nome_ficheiro):
    """Carrega o stock de produtos do ficheiro JSON."""
    try:
        with open(nome_ficheiro, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o ficheiro não existir ou estiver vazio/corrompido, retorna uma lista vazia.
        return []

def gravar_stock(nome_ficheiro, stock):
    """Grava o stock atualizado no ficheiro JSON."""
    with open(nome_ficheiro, 'w') as f:
        json.dump(stock, f, indent=2)

def formatar_saldo(saldo_cents):
    """Formata o saldo em cêntimos para o formato 'XeYc'."""
    euros = int(saldo_cents // 100)
    cents = int(saldo_cents % 100)
    return f"{euros}e{cents:02d}c"

def parse_moedas(texto_moedas):
    """Interpreta as moedas inseridas pelo utilizador e retorna o valor em cêntimos."""
    total_cents = 0
    moedas = [m.strip().lower() for m in texto_moedas.split(',')]
    
    for moeda in moedas:
        if 'e' in moeda:
            valor = float(moeda.replace('e', '').replace(',', '.')) * 100
        elif 'c' in moeda:
            valor = float(moeda.replace('c', ''))
        else:
            # Assume que valores sem unidade são euros se > 2, caso contrário cêntimos
            try:
                valor_num = float(moeda)
                if valor_num > 2:
                    valor = valor_num * 100
                else:
                    valor = valor_num
            except ValueError:
                valor = 0 # Ignora entradas inválidas
        total_cents += valor
        
    return total_cents

def calcular_troco(saldo_cents):
    """Calcula as moedas do troco a partir do saldo em cêntimos."""
    troco = {}
    moedas_disponiveis = [200, 100, 50, 20, 10, 5, 2, 1] # Em cêntimos
    
    for moeda in moedas_disponiveis:
        if saldo_cents >= moeda:
            quantidade = saldo_cents // moeda
            troco[moeda] = quantidade
            saldo_cents %= moeda
            
    return troco

def listar_produtos(stock):
    """Apresenta a lista de produtos de forma formatada."""
    print("maq:")
    print(f"{'cod':<5} | {'nome':<25} | {'quantidade':<12} | {'preço':<10}")
    print("-" * 60)
    for produto in stock:
        preco_formatado = f"{produto['preco']:.2f}€"
        print(f"{produto['cod']:<5} | {produto['nome']:<25} | {produto['quant']:<12} | {preco_formatado:<10}")

def adicionar_produto(stock, args):
    """Adiciona um novo produto ou atualiza a quantidade de um existente."""
    if len(args) != 4:
        print("maq: Uso: ADICIONAR <cod> <nome> <quantidade> <preco>")
        return
    
    cod, nome, quant_str, preco_str = args
    
    try:
        quant = int(quant_str)
        preco = float(preco_str)
    except ValueError:
        print("maq: Quantidade e preço devem ser números.")
        return

    # Verifica se o produto já existe
    for produto in stock:
        if produto['cod'] == cod:
            produto['quant'] += quant
            print(f"maq: Stock do produto '{nome}' atualizado para {produto['quant']}.")
            return
            
    # Se não existe, adiciona um novo
    novo_produto = {
        "cod": cod,
        "nome": nome.replace("_", " "), # Permite nomes com espaços
        "quant": quant,
        "preco": preco
    }
    stock.append(novo_produto)
    print(f"maq: Novo produto '{nome}' adicionado ao stock.")


def main():
    """Função principal que executa a simulação da máquina de vending."""
    stock = carregar_stock(NOME_FICHEIRO_STOCK)
    saldo_cents = 0
    
    data_atual = datetime.date.today().strftime("%Y-%m-%d")
    print(f"maq: {data_atual}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    while True:
        entrada = input(">> ").strip().upper()
        partes = entrada.split()
        comando = partes[0] if partes else ""

        if comando == "LISTAR":
            listar_produtos(stock)
        
        elif comando == "MOEDA":
            if len(partes) > 1:
                valor_adicionado = parse_moedas(" ".join(partes[1:]))
                saldo_cents += valor_adicionado
                print(f"maq: Saldo = {formatar_saldo(saldo_cents)}")
            else:
                print("maq: Por favor, insira as moedas (ex: MOEDA 1e, 20c).")

        elif comando == "SELECIONAR":
            if len(partes) == 2:
                cod_produto = partes[1]
                produto_encontrado = None
                for p in stock:
                    if p['cod'] == cod_produto:
                        produto_encontrado = p
                        break
                
                if not produto_encontrado:
                    print("maq: Produto inexistente.")
                else:
                    preco_cents = produto_encontrado['preco'] * 100
                    if produto_encontrado['quant'] == 0:
                        print(f"maq: Produto '{produto_encontrado['nome']}' esgotado.")
                    elif saldo_cents >= preco_cents:
                        saldo_cents -= preco_cents
                        produto_encontrado['quant'] -= 1
                        print(f"maq: Pode retirar o produto dispensado \"{produto_encontrado['nome']}\"")
                        print(f"maq: Saldo = {formatar_saldo(saldo_cents)}")
                    else:
                        print("maq: Saldo insuficiente para satisfazer o seu pedido.")
                        print(f"maq: Saldo = {formatar_saldo(saldo_cents)}; Pedido = {formatar_saldo(preco_cents)}")
            else:
                print("maq: Por favor, selecione um código de produto (ex: SELECIONAR A23).")

        elif comando == "ADICIONAR":
            adicionar_produto(stock, partes[1:])

        elif comando == "SAIR":
            if saldo_cents > 0:
                troco = calcular_troco(saldo_cents)
                troco_str_list = []
                for moeda, quant in troco.items():
                    if moeda >= 100:
                        troco_str_list.append(f"{quant}x {moeda//100}e")
                    else:
                        troco_str_list.append(f"{quant}x {moeda}c")
                print(f"maq: Pode retirar o troco: {', '.join(troco_str_list)}.")
            
            gravar_stock(NOME_FICHEIRO_STOCK, stock)
            print("maq: Até à próxima")
            sys.exit()

        elif comando == "":
            pass # Ignora linhas em branco

        else:
            print("maq: Comando não reconhecido. Comandos disponíveis: LISTAR, MOEDA, SELECIONAR, ADICIONAR, SAIR.")

if __name__ == "__main__":
    main()