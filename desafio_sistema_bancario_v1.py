menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        print("Depósito")
        
        valor = float(input("Valor para depósito: R$ "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Valor inválido!")

    elif opcao == "s":
        print("Saque")
        
        valor = float(input("Valor para saque: R$ "))
                
        if valor > saldo:
            print("Sem saldo suficiente.")
        elif valor > limite:
            print(f"O limite para saque é de R$ {limite:.2f} por")
        elif numero_saques >= LIMITE_SAQUES:
            print("Quantidade de saques excedida.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        else:
            print("Valor inválido!")

    elif opcao == "e":
        # print("Extrato")
        
        print("\n************** E X T R A T O ***************")
        print("Não existem movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("********************************************")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")