

from db.vendas_db import buscar_produto_para_venda, finalizar_venda, listar_produtos_para_venda


def ler_int(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        print("\n[ERRO] Digite apenas numeros inteiros.")
        return None


def mostrar_mensagem(titulo, mensagem):
    print("\n" + "=" * 55)
    print(titulo.center(55))
    print("-" * 55)
    print(mensagem.center(55))
    print("=" * 55)


def exibir_catalogo_venda():
    produtos = listar_produtos_para_venda()

    print("\n==================== CATALOGO DE PRODUTOS ====================")

    if len(produtos) == 0:
        print("Nenhum produto ativo disponivel para venda.")
        print("==============================================================")
        return

    print(f"{'ID':<5} {'Produto':<25} {'Preco':>12} {'Estoque':>10}")
    print("-" * 58)

    for produto in produtos:
        print(
            f"{produto[0]:<5} "
            f"{produto[1][:25]:<25} "
            f"R$ {produto[2]:>8.2f} "
            f"{produto[3]:>10}"
        )

    print("==============================================================")


def mostrar_carrinho(carrinho):
    if len(carrinho) == 0:
        mostrar_mensagem("CARRINHO", "Carrinho vazio.")
        return

    total = 0

    print("\n========================= CARRINHO =========================")
    print(f"{'ID':<5} {'Produto':<22} {'Qtd':>5} {'Unitario':>12} {'Subtotal':>12}")
    print("-" * 60)

    for item in carrinho:
        total += item["subtotal"]

        print(
            f"{item['id_produto']:<5} "
            f"{item['nome'][:22]:<22} "
            f"{item['quantidade']:>5} "
            f"R$ {item['preco_unitario']:>8.2f} "
            f"R$ {item['subtotal']:>8.2f}"
        )

    print("-" * 60)
    print(f"{'TOTAL:':>46} R$ {total:>8.2f}")
    print("=" * 60)


def adicionar_item(carrinho):
    exibir_catalogo_venda()

    id_produto = ler_int("Digite o ID do produto: ")

    if id_produto is None:
        return

    quantidade = ler_int("Digite a quantidade: ")

    if quantidade is None:
        return

    if quantidade <= 0:
        mostrar_mensagem("ERRO", "Quantidade invalida.")
        return

    produto = buscar_produto_para_venda(id_produto)

    if produto is None:
        mostrar_mensagem("ERRO", "Produto nao encontrado ou inativo.")
        return

    id_produto_banco = produto[0]
    nome = produto[1]
    preco_venda = produto[2]
    estoque = produto[3]

    quantidade_no_carrinho = sum(
        item["quantidade"]
        for item in carrinho
        if item["id_produto"] == id_produto_banco
    )

    estoque_disponivel = estoque - quantidade_no_carrinho

    if quantidade > estoque_disponivel:
        mostrar_mensagem("ERRO", f"Estoque disponivel: {estoque_disponivel}")
        return

    subtotal = quantidade * preco_venda

    carrinho.append({
        "id_produto": id_produto_banco,
        "nome": nome,
        "quantidade": quantidade,
        "preco_unitario": preco_venda,
        "subtotal": subtotal
    })

    mostrar_mensagem("SUCESSO", "Produto adicionado ao carrinho.")


def finalizar_carrinho(carrinho):

    if len(carrinho) == 0:
        mostrar_mensagem("ERRO", "Nao existe item no carrinho.")
        return False

    mostrar_carrinho(carrinho)

    confirmar = input("Deseja finalizar a venda? (s/n): ").lower().strip()

    if confirmar != "s":
        mostrar_mensagem("AVISO", "Venda nao finalizada.")
        return False
    
    #Atualizamos a chamada da função para enviar apenas o carrinho

    venda_finalizada = finalizar_venda(carrinho)

    if venda_finalizada:
        carrinho.clear()
        mostrar_mensagem("SUCESSO", "Venda finalizada com sucesso.")
        return True

    mostrar_mensagem("ERRO", "Venda nao foi finalizada.")
    return False


def fluxo_registrar_venda():
    carrinho = []

    while True:
        print("""
        _____________________________________
        |          CARRINHO DE VENDA        |
        |===================================|
        |    |1| - Adicionar item           |
        |    |2| - Ver carrinho             |
        |    |3| - Finalizar venda          |
        |    |4| - Cancelar venda           |
        |___________________________________|
        """)

        opcao = ler_int("Escolha uma opcao: ")

        if opcao is None:
            continue

        elif opcao == 1:
            adicionar_item(carrinho)

        elif opcao == 2:
            mostrar_carrinho(carrinho)

        elif opcao == 3:
            finalizou = finalizar_carrinho(carrinho)

            if finalizou:
                return True

        elif opcao == 4:
            carrinho.clear()
            mostrar_mensagem("VENDA CANCELADA", "Carrinho limpo. Voltando ao menu principal.")
            return True

        else:
            print("Opcao invalida.")


def menu_venda():
    while True:
        print("""
        _____________________________________
        |            MENU VENDA             |
        |===================================|
        |    |1| - Registrar Venda          |
        |    |0| - Sair Para Menu Principal |
        |___________________________________|
        """)

        opcao = ler_int("Escolha uma opcao: ")

        if opcao is None:
            continue

        elif opcao == 0:
            break

        elif opcao == 1:
            sair_para_menu_principal = fluxo_registrar_venda()

            if sair_para_menu_principal:
                break

        else:
            print("Opcao invalida.")