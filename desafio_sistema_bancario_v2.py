def depositar(valor, numero_conta, contas, /):# positional only
    conta, i = filtrar_conta(numero_conta, contas)
    
    if conta:            
        if valor > 0:
            contas[i]["saldo"] += valor
            contas[i]["extrato"] += f"Depósito:\tR$ {valor:.2f}\n"
            
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    else:
        print("\n@@@ Operação falhou! A conta informada é inválida. @@@")

    return contas

def sacar(*, valor, numero_conta, contas): # keyword only
    conta, i = filtrar_conta(numero_conta, contas)
    
    if conta:
        if valor > conta["saldo"]:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > conta["limite"]:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif conta["limite_saques"] <= 0:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        elif valor > 0:
            contas[i]["saldo"] -= valor
            contas[i]["extrato"] += f"Saque:\t\tR$ {valor:.2f}\n"
            contas[i]["limite_saques"] -= 1
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return contas

#visualizar histórico    
def visualizar_extrato(contas, /, *, numero_conta):
    conta_filtrada, indice = filtrar_conta(numero_conta, contas)
    if conta_filtrada:
      print("\n================ E X T R A T O ================")
      print("Não foram realizadas movimentações." if not conta_filtrada["extrato"] else conta_filtrada["extrato"])
      print(f"\nSaldo:\t\tR$ {conta_filtrada["saldo"]:.2f}")
      print("=================================================")
    else:
      print("\n@@@ Conta não encontrada! @@@")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios, limite, limite_saques):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "limite_saques": limite_saques, "extrato": "", "limite": limite, "ativa":True}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    
def inativar_conta(numero_conta, contas):
  conta, i = filtrar_conta(numero_conta, contas)
  
  if conta:
      contas[i]["ativa"]=False
  else:
      print("\n@@@ Conta não encontrada! @@@")
      
  return contas

def filtrar_conta(numero_conta, contas):
    contas_filtradas = [conta for conta in contas if conta["numero_conta"] == numero_conta]
    return contas_filtradas[0], contas.index(contas_filtradas[0]) if contas_filtradas else None
    
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            Saldo:\t{conta['saldo']}
            Ativa:\t{conta['ativa']}
        """
        print("=" * 100)
        print(linha)

def listar_usuarios(usuarios, contas):
    for usuario in usuarios:
        linha = f"""\
            Nome: {usuario['nome']}
            Data Nascimento: {usuario['data_nascimento']}
            CPF: {usuario['cpf']}
            Endereco: {usuario['endereco']}
        """
        # buscar a(s) conta(s) cadastrada(s) para esse usuário
        contas_cliente = [conta for conta in contas if conta["usuario"]["cpf"] == usuario["cpf"]]
        if contas_cliente:
            linha += "\nContas\n"
            for conta in contas_cliente:
                linha += f"""              
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
                Saldo:\t{conta['saldo']}
                Ativa:\t{conta['ativa']}
            """
        
        print("=" * 100)
        print(linha)
  

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    limite = 500
    usuarios = []
    contas = []

    menu = """\n
    ================ MENU ================
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato*
    [nc] Nova conta
    [xc] Inativar conta
    [lc] Listar contas
    [nu] Novo usuário
    [lu] Listar usuários
    [q]  Sair
    => """
    
    while True:
        
        match input(menu):
          case "d":
              numero_conta = int(input("Informe a conta a depositar: "))
              valor = float(input("Informe o valor do depósito: "))              
              contas = depositar(valor, numero_conta, contas)

          case "s":
            numero_conta = int(input("Informe a conta a sacar: "))
            valor = float(input("Informe o valor do saque: "))
            
            contas = sacar(
                valor=valor,
                numero_conta = numero_conta,
                contas = contas)

          case "e":
           # exibir_extrato(saldo, extrato=extrato)
           numero_conta = int(input("Informe a conta: "))
           visualizar_extrato(contas, numero_conta=numero_conta)

          case "nu":
            criar_usuario(usuarios)
            
          case "lu":
            listar_usuarios(usuarios, contas)

          case "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios, limite, LIMITE_SAQUES)

            if conta:
                contas.append(conta)
          case "xc":
              numero_conta = int(input("Informe a conta a inativar: "))
              contas = inativar_conta(numero_conta, contas)
          
          case "lc":
            listar_contas(contas)

          case "q":
            break

          case __:
            print("Opção inválida!")


if __name__ == "__main__":    
    main()    