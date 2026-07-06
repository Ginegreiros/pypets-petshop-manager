

try:
    from db.produtos_db  import cad_prod 
except ImportError:
    print("Erro ao exportar informações")
    cad_prod = None

try:
    from db.clientes_db import cad_cliente 
except ImportError:
    print("Erro ao exportar informações")
    cad_cliente = None

try:
    from db.clientes_db import alt_cliente 
except ImportError:
    print("Erro ao exportar informações")
    alt_cliente = None

try:
    from db.clientes_db import desat_cliente 
except ImportError:
    print("Erro ao exportar informações")
    desat_cliente = None

try:
    from db.clientes_db import ativar_cliente 
except ImportError:
    print("Erro ao exportar informações")
    ativar_cliente = None

try:
    from db.pets_db import cad_pet 
except ImportError:
    print("Erro ao exportar informações")
    cad_pet = None

try:
    from db.pets_db import alt_pet 
except ImportError:
    print("Erro ao exportar informações")
    alt_pet = None

def menu_cadastro():

    while True:

        print("""
        ________________________________________
        |             MENU CADASTRO            |
        |--------------------------------------|                                    
        |  |1| - Cadastrar Novo Produto        |
        |  |2| - Cadastrar Novo Cliente        |
        |  |3| - Alterar informações Cliente   |
        |  |4| - Desativar Cliente             |
        |  |5| - Ativar Cliente                |
        |  |6| - Cadastrar Novo Pet            |
        |  |7| - Alterar informações Pet       |
        |  |0| - Voltar ao Menu Principal      |
        |______________________________________|
    """)
        
        opcao = input("Digite a opção desejada: ").strip()
        
        if opcao == "0":
            break
        elif opcao == "1":
            cad_prod()
        elif opcao == "2":
            cad_cliente()
        elif opcao == "3":
            alt_cliente()
        elif opcao == "4":
            desat_cliente()
        elif opcao == "5":
            ativar_cliente()
        elif opcao == "6":
            cad_pet()  
        elif opcao == "7":
            alt_pet()
        else:
            print("Opção inválida. Por favor, escolha um número do menu.")