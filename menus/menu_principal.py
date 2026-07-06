

# import sys, apenas para encerrar o programa 
#o código chama a função sys.exit(0) para encerrar o programa de forma limpa e imediata, caso o usuário escolha a opção de sair do menu principal.
import sys 


# Como ainda não tenho os arquivos, usarei blocos try-except para evitar erros de importação. E o sistema vai me alertar que o modulo está em construção.

# |clientes|
try: 

    from menus import menu_cadastro

except ImportError as e:
    print(e)
    menu_cadastro = None

# |produtos|
try:
    from menus import menu_estoque 
except ImportError as e:
    print(e)
    menu_estoque = None

#| serviços|
try:
    from menus import menu_agendamento
except ImportError as e:
    print(e)
    menu_agendamento = None
    

# |vendas|
try:
    from menus import menu_venda
except ImportError as e:
    print(e)
    menu_venda = None

# |financeiro|
try:
    from menus import menu_financeiro
except ImportError as e:
    print(e)
    menu_financeiro = None

# =========================================
# MENU PRINCIPAL (Navegação central)
# =========================================

def exibir_menu_principal():

    while True:
        
        print(f"""
        _____________________________________
        |              PY PETS              |
        |   O Porto Seguro para o seu Pet!  |
        |===================================|
        |         |1| - Cadastro            |
        |         |2| - Agendamento         |
        |         |3| - Vendas              |
        |         |4| - Estoque             |
        |         |5| - Financeiro          |
        |         |0| - Sair                |
        |___________________________________|
        """)

        try:

            opcao = int(input("Escolha uma opção: "))

            if opcao == 0:
                print("Saindo do programa...")
                sys.exit(0)

            elif opcao == 1: 
                if menu_cadastro is not None:
                    menu_cadastro.menu_cadastro()
                else: 
                    print("\n[Aviso] Módulo de Cadastro em construção.")


            elif opcao == 2:
                if menu_agendamento is not None:
                    menu_agendamento.menu_agendamento()
                else:
                    print("\n[Aviso] Módulo de Agendamento em construção.")

            elif opcao == 3:
                if menu_venda is not None:
                    menu_venda.menu_venda()
                else:
                    print("\n[Aviso] Módulo de Vendas em construção.")
                    
            elif opcao == 4:
                if menu_estoque is not None:
                    menu_estoque.menu_estoque()
                else:
                    print("\n[Aviso] Módulo de Estoque em construção.")

            elif opcao == 5:
                if menu_financeiro is not None:
                    menu_financeiro.menu_financeiro()
                else:
                    print("\n[Aviso] Módulo Financeiro em construção.")
            else:
                print("\n[Erro] Opção inválida. Por favor, escolha uma opção válida.")
        
        except ValueError:
            #Blindagem exigida contra letras em vez de números inteiros. O programa vai exibir uma mensagem de erro e solicitar que o usuário digite novamente a opção.
            print("\n[Erro] Entrada inválida. Por favor, digite apenas números inteiros.")
        
        except KeyboardInterrupt:
            #Proteção caso o usuário aperte Ctrl+C para interromper a execução do programa acidentalmente. O programa vai exibir uma mensagem de erro e encerrar a execução de forma limpa.
            print("\n[Erro] Operação interrompida pelo usuário. Saindo do programa...")
            sys.exit(0)