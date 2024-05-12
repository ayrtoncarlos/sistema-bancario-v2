import re
from datetime import datetime
from pprint import pprint


def criar_usuario() -> None:
    global NOME, CONTAS, clientes, validador_cliente
    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento: ")
    cpf = input("CPF: ")
    cpf = re.sub('[^0-9]', '', cpf)
    logradouro = input("Logradouro: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")

    endereco = {
        "logradouro": logradouro,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado
    }

    senha = input("Defina uma senha: ")

    if cpf not in clientes.keys():
        clientes[cpf] = {
            NOME: nome,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
            CONTAS: []
        }
        validador_cliente[cpf] = senha
        print("Usuário cadastrado com sucesso!")
    else:
        print("O CPF informado já havia sido cadastrado anteriormente.")


def criar_conta_corrente(cpf: str) -> None:
    global CONTAS, NUMERO_CONTA, NUMERO_SAQUES, SALDO, EXTRATOS, clientes, numero_conta_corrente

    if cpf in clientes.keys():
        contas = clientes[cpf][CONTAS]
        nova_conta = {
            "agencia": "0001",
            NUMERO_CONTA: numero_conta_corrente,
            SALDO: 0,
            NUMERO_SAQUES: 0,
            EXTRATOS: []
        }
        contas.append(nova_conta)
        clientes[cpf][CONTAS] = contas
        numero_conta_corrente += 1
        print("Conta corrente criada com sucesso!")
    else:
        print(f"Não foi encontrado nenhum cliente cadastrado com o CPF: {cpf}.")


def validar_usuario(cpf: str, senha: str) -> bool:
    if cpf in validador_cliente.keys():
        if cpf in clientes.keys():
            return True
    return False

def extrato(operacao: str, saldo_atual: float, valor: float, /, *, extratos: list) -> list:
    global DEPOSITO, SAQUE
    novo_saldo = 0

    if operacao == DEPOSITO:
        novo_saldo = (saldo_atual + valor)
    elif operacao == SAQUE:
        novo_saldo = (saldo_atual - valor)

    extrato = {
        "operação": operacao,
        "valor": f'R$ {valor:.2f}',
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "saldo_antes": f'R$ {saldo_atual:.2f}',
        "saldo_depois": f'R$ {novo_saldo:.2f}'
    }

    extratos.append(extrato)

    return extratos


def visualizar_historico(*, extratos: list) -> None:
    if len(extratos) > 0:
        for extrato in extratos:
            pprint(extrato)
    else:
        print("Não foram realizadas movimentações.")


def visualizar_contas_correntes(contas: list) -> list:
    indices_contas = []
    if len(contas) > 0:
        for indice, conta in enumerate(contas):
            print(indice + 1, conta)
            indices_contas.append(indice + 1)
    else:
        print("Não há nenhuma conta disponível para esse cliente.")
    return indices_contas


def depositar(saldo_atual: float, valor: float, extratos: list, /) -> (float, list):
    global DEPOSITO

    if valor > 0:
        extratos = extrato(DEPOSITO, saldo_atual, valor, extratos=extratos)
        saldo_atual = saldo_atual + valor
        print("Depósito feito com sucesso!")
        print(f'Novo saldo: {saldo_atual:.2f}')
    else:
        print("Valor inválido, por favor inserir valores acima de 0.")

    return saldo_atual, extratos


def sacar(*, saldo_atual: float, valor: float, numero_saques: int, extratos: list) -> (float, int, list):
    global VALOR_LIMITE

    if valor <= VALOR_LIMITE:
        if (saldo_atual - valor) >= 0:
            extratos = extrato(SAQUE, saldo_atual, valor, extratos=extratos)
            saldo_atual = saldo_atual - valor
            numero_saques += 1
            print("Saque feito com sucesso!")
            print(f'Novo saldo: {saldo_atual:.2f}')
        else:
            print("Não será possível sacar o valor informado, pois não há saldo suficiente.")
    else:
        print(f'Valor inserido é maior que o valor limite de R$ {VALOR_LIMITE:.2f}')

    return saldo_atual, numero_saques, extratos


menu_1 = """
[u] Criar Usuário
[c] Criar Conta Corrente
[l] Entrar
[q] Sair

=> """

menu_2 = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

SALDO = "saldo"
VALOR_LIMITE = 500
LIMITE_SAQUES = 3
DEPOSITO = "Depósito"
SAQUE = "Saque"
NOME = "nome"
CONTAS = "contas"
NUMERO_CONTA = "numero_conta"
EXTRATOS = "extratos"
NUMERO_SAQUES = "numero_saques"
clientes = {}
validador_cliente = {}
numero_conta_corrente = 1

print(" SISTEMA BANCÁRIO ".center(30, '#'))

while True:

    opcao_1 = input(menu_1).lower()

    if opcao_1 == 'u':
        criar_usuario()

    elif opcao_1 == 'c':
        cpf = input("CPF: ")
        cpf = re.sub('[^0-9]', '', cpf)
        senha = input("Senha: ")

        isValido = validar_usuario(cpf, senha)

        if isValido:
            criar_conta_corrente(cpf)
        else:
            print("CPF ou Senha inválida, por favor tentar novamente.")

    elif opcao_1 == 'l':
        cpf = input("CPF: ")
        cpf = re.sub('[^0-9]', '', cpf)
        senha = input("Senha: ")

        isValido = validar_usuario(cpf, senha)

        if isValido:

            cliente = clientes[cpf]

            print(f" BEM VINDO {cliente[NOME]}! ".center(30, '#'))
            print(" Contas Disponíveis ".center(30, '#'))

            indices_contas = visualizar_contas_correntes(cliente[CONTAS])

            if len(indices_contas) > 0:

                conta_selecionada = int(input("Selecione a conta que deseja utilizar: "))

                if conta_selecionada in indices_contas:

                    conta = cliente[CONTAS][conta_selecionada - 1]

                    while True:
                        print(f" Usuário: {cliente[NOME]} ".center(30, '#'))
                        print(f" Conta: {conta[NUMERO_CONTA]} | Saldo: {conta[SALDO]} ".center(30, '#'))

                        opcao_2 = input(menu_2).lower()

                        if opcao_2 == 'd':
                            print(f" {DEPOSITO} ".center(30, '#'))
                            valor = float(input("Insira o valor para depósito: R$ "))
                            conta[SALDO], conta[EXTRATOS] = depositar(conta[SALDO], valor, conta[EXTRATOS])

                        elif opcao_2 == 's':
                            print(f" {SAQUE} ".center(30, '#'))

                            if conta[NUMERO_SAQUES] < LIMITE_SAQUES:
                                valor = float(input("Insira o valor para saque: R$ "))
                                conta[SALDO], conta[NUMERO_SAQUES], conta[EXTRATOS] = sacar(saldo_atual=conta[SALDO],
                                                                                            valor=valor,
                                                                                            numero_saques=conta[NUMERO_SAQUES],
                                                                                            extratos=conta[EXTRATOS])
                            else:
                                print("Número de saques diários foi excedido.")

                        elif opcao_2 == 'e':
                            print(" Extrato ".center(30, '#'))
                            visualizar_historico(extratos=conta[EXTRATOS])
                            print(f'Saldo atual: R$ {conta[SALDO]:.2f}')

                        elif opcao_2 == 'q':
                            break

                        else:
                            print("Operação inválida, por favor selecione novamente a operação desejada.")
                        
                        print("#".center(30, '#'))

                else:
                    print("Conta selecionada é inválida.")

        else:
            print("CPF ou Senha inválida, por favor tentar novamente.")

    elif opcao_1 == 'q':
        print(" FIM ".center(30, '#'))
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

    print("#".center(30, '#'))
