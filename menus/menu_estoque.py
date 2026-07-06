

try:
    from db.produtos_db import  alt_infos
except ImportError:
    print("Erro ao exportar informações")
    alt_infos = None

try:
    from db.produtos_db import desativ_prod
except ImportError:
    print("Erro ao exportar informações")
    desativ_prod = None

try:
    from db.produtos_db import ativ_prod
except ImportError:
    print("Erro ao exportar informações")
    ativ_prod = None

try:
    from db.produtos_db import repor_lote
except ImportError:
    print("Erro ao exportar informações")
    repor_lote = None

try:
    from relatorios.filtros import search
except ImportError:
    print("Erro ao exportar informações")
    search = None

try:
    from relatorios.filtros import cat_orden
except ImportError:
    print("Erro ao exportar informações")
    cat_orden = None

try:
    from relatorios.filtros import exibir_catalogo
except ImportError:
    print("Erro ao exportar informações")
    exibir_catalogo = None

try: 
    from db.produtos_db import listar_produtos_simples
except ImportError:
    print("Erro ao exportar informações")
    listar_produtos_simples = None


def menu_estoque():
    while True:
    
        print(f"""
        ________________________________________
        |             MENU ESTOQUE             |
        |======================================|
        |  |1| - Alterar Informações Gerais    |
        |  |2| - Desativar Produto             |
        |  |3| - Reativar Produto              |
        |  |4| - Reposição Por Lote            |
        |  |5| - Guia de pesquisa              |
        |  |6| - Exibir Catalogo de Produtos   |
        |  |7| - Catalogo Ordenado             |
        |  |0| - Sair Para Menu Principal      |
        |______________________________________|
        """)

        opcao = input("Digite a opção desejada: ")

        if opcao == "0":
            break
        elif opcao == "1":
            alt_infos()
        elif opcao == "2":
            desativ_prod()
        elif opcao == "3":
            ativ_prod()
        elif opcao == "4":

            if listar_produtos_simples:
                listar_produtos_simples()

            try:
                qtd_add = int(input("Quantidade a adicionar: "))

                ids = input(
                    "IDs dos produtos separados por vírgula: "
                )

                ids_alvo = [
                    int(i.strip())
                    for i in ids.split(",")
                ]
            except ValueError:
                print("ERRO: digite apenas números inteiros.")
                continue
            repor_lote(qtd_add, *ids_alvo)

        elif opcao == "5":
            search()
        elif opcao == "6":
            exibir_catalogo()
        elif opcao == "7":
            cat_orden()
        
        else:
            print("Opção inválida. Tente novamente.")