
# import sys é necessário para permitir a saída do programa com sys.exit(0)
import sys

try: 
    from db.financeiro_db import buscar_ranking_produtos
except ImportError:
    buscar_ranking_produtos = None
#====================================
try: 
    from db.financeiro_db import buscar_dados_bi
except ImportError:
    buscar_dados_bi = None
#=================================
try: 
    from relatorios.exportar_relatorio import gerar_txt_fechamento
except ImportError:
    gerar_txt_fechamento = None
#=================================
try:
    from db.financeiro_db import buscar_nota_fiscal
except ImportError:
    buscar_nota_fiscal = None
#=================================
try:
    from db.financeiro_db import buscar_ranking_servicos
except ImportError:
    buscar_ranking_servicos = None
#=============================
try:
    from db.financeiro_db import buscar_promocoes
except ImportError:
    buscar_promocoes = None
#==============================
try:
    from db.financeiro_db import aplicar_promocao
except ImportError:
    aplicar_promocao = None
#==============================

try:
    from db.financeiro_db import remover_promocao
except ImportError:
    remover_promocao = None
#==============================

try:
    from db.vendas_db import listar_vendas
except ImportError:
    listar_vendas = None
#=================================

try: 
    from db.produtos_db import listar_produtos_simples
except ImportError:
    listar_produtos_simples = None
    
def menu_financeiro():
    
    while True:
        print(f"""
        ____________________________________________
        |    FINANCEIRO & BUSINESS INTELLIGENCE    |
        |==========================================|
        |  |1| - Exibir Nota Fiscal                |
        |  |2| - Relatório Expresso                |
        |  |3| - Promoções                         |
        |  |4| - Painel BI                         |
        |  |5| - Ranking de Produtos/Serviços      |
        |  |6| - Export. Relat. de Fechamento TXT  |
        |  |0| - Sair Para Menu Principal          |
        |__________________________________________|
        """)

        try:

            opcao = int(input("Escolha uma opção:"))

            if opcao == 0:
                print("Retornando ao Menu Principal...")
                break

            elif opcao == 1:

                if buscar_nota_fiscal:
                    exibir_nota_fiscal()
                else:
                    print("\n[Aviso] Módulo e Nota Fiscal indisponível.")

            elif opcao == 2:
                if buscar_dados_bi:
                    gerar_relatorio_expresso()
                else:
                    print("\n[Aviso] Módulo de Relatório Expresso indisponível.")

                # Futuramente: chamará exportar_relatorio.gerar()

            elif opcao == 3:
                if buscar_promocoes and aplicar_promocao and remover_promocao:
                    submenu_promocoes()
                else:
                    print("\n[Aviso] Módulo de promoções indisponível.")
                # Futuramente: chamará exportar_relatorio.gerar_promocoes()

            elif opcao == 4:
                if buscar_dados_bi:
                    exibir_painel_bi()
                else:
                    print("\n[Aviso] Módulo de Painel BI indisponível.")

            elif opcao == 5:
                
                if buscar_ranking_produtos and buscar_ranking_servicos:
                    exibir_ranking()
                else:
                    print("\n[Aviso] Banco de dados Ranking de Produtos/Serviços indisponível.")
                    # Futuramente: chamará buscar_ranking_produtos.exibir_ranking()

            elif opcao == 6:
                if gerar_txt_fechamento:
                    gerar_txt_fechamento()
                else:
                    print("\n[Aviso] Módulo de exportação de texto indisponível.")
                    
            else: 
                print("Opção inválida. Tente novamente.")

        except ValueError:
            print("\n [ERRO DE DIGITAÇÃO] Por favor, insira apenas números inteiros para selecionar uma opção.") #Blindagem exigida pelo professor contra letras em campos numéricos.

        except KeyboardInterrupt:
            print("\n[ERRO] Operação interrmpida pelo usuário. Encerrando de forma limpa...")
            sys.exit(0)

def exibir_ranking():

    ranking_produtos = buscar_ranking_produtos()
    ranking_servicos = buscar_ranking_servicos()


    print("\n")
    print("=" * 40)
    print("\n   RANKING DE PRODUTOS  ")
    print("=" * 40)
     

    if not ranking_produtos:
        
        print("Nenhum produto encontrado.")
        return
    else:
        for posicao, produto in enumerate(ranking_produtos, start=1):

            nome = produto[0]
            quantidade = produto[1]
            faturamento = produto[2]

            print(f"""
_____________________________________
{posicao}º Lugar                  
Produto: {nome}                   
Quantidade Vendida:{quantidade}   
Faturamento: R$ {faturamento:.2f} 
___________________________________
""")
            

    print("\n")
    print("=" * 40)
    print("\n   RANKING DE SERVIÇOS  ")
    print("=" * 40)
    
    if not ranking_servicos:
        print("Nenhum serviço encontrado.")
        return
    
    else:


        for posicao, produto in enumerate(ranking_servicos, start=1):

            nome = produto[0]
            quantidade = produto[1]
            faturamento = produto[2]

            print(f"""
_____________________________________
{posicao}º Lugar                  
Serviço: {nome}                   
Atendimentos: {quantidade}        
Faturamento: R$ {faturamento:.2f} 
_____________________________________

                """)


def exibir_painel_bi():
    
    dados = buscar_dados_bi()

    if not dados:
        print("Nenhum dado encontrado.")
        return
    print(f"""
_____________________________________________
            PAINEL BI GERENCIAL            
===========================================
Total de vendas: {dados['total_vendas']}  
Faturamento: R$ {dados['faturamento']:.2f}
Margem de Lucro: R$ {dados['margem_lucro']:.2f} 
___________________________________________
""")

def exibir_nota_fiscal():

    # Esqueleto visual para a opção 1

    print("\n === EMISSÃO DE NOTA FISCAL ===")

    if listar_vendas:
        vendas = listar_vendas()

        if not vendas:
            print("Nenhuma venda registrada no sistema para emitir nota.")
            return
        
        print("\n --- Vendas Disponíveis ---")

        for v in vendas:
            id_v, data_v, valor_t, status_v = v
            status_str = "Ativa" if status_v == 1 else "Cancelada"
            print(f"""
ID: {id_v}
Data: {data_v.strftime('%d/%m/%Y %H:%M')}
Valor: R${valor_t:.2f}
Status: {status_str}
""")

        print("-----------------------------------\n")
    
    else:
        print("Aviso: Função de listagem de vendas não disponível.")
        return
    

    try:

        id_venda = int(input("\nDigite o ID da venda: "))

        dados = buscar_nota_fiscal(id_venda)

        if not dados:
            print("\nVenda não encontrada ou inativa.")
            return
        

        venda = dados["venda"]
        itens = dados["itens"]

        # 1. CABEÇALHO ÚNICO (Impresso fora e antes do laço de repetição)
        print(f"""
________________________________________
             NOTA FISCAL           
========================================
Venda ID: {venda[0]}
Data/Hora: {venda[1]}
========================================
        ITENS DA COMPRA:""")

        for item in itens:
            nome = item[0]
            qtd= item[1]
            preco = item[2]
            subtotal = qtd * preco

            print(f"""
Nome: {nome[:22]:<22} 
Qtd: x{qtd:>2}  
Preço: R${preco:>6.2f}
Subtotal: R${subtotal:>7.2f}
""")
        
        print(f"""
======================================= 
VALOR TOTAL DESTA NOTA: R$ {venda[2]:.2f}
======================================
        """)       
        
    except ValueError:
        print("ERRO: ID da venda deve ser um número inteiro.")
        return
    
def gerar_relatorio_expresso():

    dados = buscar_dados_bi()

    if not dados:

        print("Nenhum dado encontrado para gerar o relatório expresso.")
        return
    
    print(f"""
___________________________________________
            RELATÓRIO EXPRESSO           
===========================================
Total de vendas: {dados['total_vendas']}
Faturamento: R${dados['faturamento']:.2f}
____________________________________________
          """)
    

def exibir_promocoes():

    promocoes = buscar_promocoes()

    print("\n === PROMOÇÕES ATIVAS === ")

    if not promocoes:

        print("Nenhuma promoção cadastrada")
        return
    
    for produto in promocoes:

        nome = produto[0]
        original = float(produto[1])
        promocao = float(produto[2])

        desconto = original - promocao

        print(f"""

    ___________________________________________
    Produto: {nome}
    ===========================================
    De: R$ {original:.2f}
    Por: R$ {promocao:.2f}
    ===========================================
    Economia: R$ {desconto:.2f}
    ___________________________________________

    """)


def submenu_promocoes():
    while True:
        print("""
        ___________________________________
        |           PROMOCOES             |
        |=================================|
        |  |1| - Listar promocoes         |
        |  |2| - Aplicar promocao         |
        |  |3| - Remover promocao         |
        |  |0| - Voltar                   |
        |_________________________________|
        """)

        try:
            opcao = int(input("\nEscolha uma opcao: "))

            if opcao == 0:
                break

            elif opcao == 1:
                exibir_promocoes()

            elif opcao == 2:

                if listar_produtos_simples:
                    listar_produtos_simples(1)
                    print("")

                id_produto = int(input("\nDigite o ID do produto: "))
                desconto = int(input("\nDigite o percentual de desconto: "))

                aplicar_promocao(id_produto, desconto)

            elif opcao == 3:
                
                # Puxa a lista de promoções ativas direto do banco
                promocoes_ativas = buscar_promocoes()
                
                if not promocoes_ativas:
                    print("\nNenhuma promoção ativa para remover.")
                    continue
                
                # Monta uma lista simples e direta só com ID e Nome
                print("\n=== PRODUTOS COM PROMOÇÃO ATIVA ===")
                for prod in promocoes_ativas:
                    # prod[0] = id, prod[1] = nome
                    print(f"ID: {prod[0]:<5} | Produto: {prod[1]}")
                print("===================================")

                id_produto = int(input("\nDigite o ID do produto para remover a promoção: "))
                remover_promocao(id_produto)

            else:
                print("Opcao invalida.")

        except ValueError:
            print("\nERRO: digite apenas numeros inteiros.")