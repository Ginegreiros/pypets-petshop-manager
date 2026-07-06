import mysql.connector
from conexao import obter_conexao

def search():
    print("\n ====================  GUIA DE PESQUISA  ====================")

    termo_busca = input("\n Digite o nome ou a categoria que deseja encontrar: ")

    try:
         # Conexão com o banco de dados
        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, categoria, preco_custo, preco_venda, qtd_estq
            FROM Produto
            WHERE status = 1 AND (
                LOWER(nome) LIKE %s OR
                LOWER(categoria) LIKE %s OR
                CAST(preco_custo as CHAR) LIKE %s OR
                CAST(preco_venda as CHAR) LIKE %s OR
                CAST(qtd_estq as CHAR) LIKE %s
                       )
        """, (f"%{termo_busca.lower()}%", f"%{termo_busca.lower()}%", f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        # Encerrando conexão com o banco de dados
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()

        if len(resultados) == 0:
            print("\n Nenhum resultado encontrado...")
        else:
            for produto in resultados:
                print(f"""
                ID: {produto[0]}
                Nome: {produto[1]}
                Categoria: {produto[2]}
                Preço de Custo: R${produto[3]:.2f}
                Preço de Venda: R${produto[4]:.2f}
                Total em Estoque: {produto[5]}
                """)

    #Método para tratar erros de conexão com o banco de dados
    #Segurando que o programa não quebre e informe o usuário sobre o erro
    except mysql.connector.Error as erro:
        print(f"\n ERRO FATAL DE CONEXAO COM BANCO DE DADOS: {erro}")
        print("\n Produto não encontrado. Tente novamente mais tarde.")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def cat_orden():
    while True:
        print("""
           _________________   
========== CATALOGO ORDENADO ===========
|        |1| Ordem Alfabética          |
|        |2| Mais Baratos Primeiro     |
|        |3| Mais Caros Primeiro       |
|        |4| Maior Estoque Primeiro    |
|        |0| Voltar ao Menu            | 
========================================
        """)

        opcao = input("\n Digite a opção desejada: ")
        if opcao == "0":
            break

        query_base = "SELECT id, nome, categoria, preco_custo, preco_venda, preco_original, preco_promocao, qtd_estq, status FROM Produto WHERE status = 1"

        if opcao == "1":
            query_base = f"{query_base} ORDER BY LOWER(nome) ASC"
        elif opcao == "2":
            query_base = f"{query_base} ORDER BY preco_venda ASC"
        elif opcao == "3":
            query_base = f"{query_base} ORDER BY preco_venda DESC" 
        elif opcao == "4":
            query_base = f"{query_base} ORDER BY qtd_estq DESC"
        else:
            print("\n Opção inválida. Tente novamente.")
            continue

        try: 
            # Conexão com o banco de dados
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query_base)
            estq_orden = cursor.fetchall()
            
            for produto in estq_orden:
                print(f"""
{'='*140}
{'ID':<5} | {'NOME':<20} | {'CATEGORIA':<15} | {'PREÇO CUSTO':<15} | {'PREÇO VENDA':<15} | {'PREÇO ORIGINAL':<15} | {'PREÇO PROMOÇÃO':<17} | {'ESTOQUE':<10} | {'STATUS':<10}
{'='*140}
{produto[0]:<5} | {produto[1]:<20} | {produto[2]:<15} | R${produto[3]:<15.2f} | R${produto[4]:<15.2f} | R${produto[5]:<15.2f} | R${produto[6]:<17.2f} | {produto[7]:<10} | {produto[8]:<10}
{'='*140}
""")

        #Método para tratar erros de conexão com o banco de dados
        #Segurando que o programa não quebre e informe o usuário sobre o erro
        except mysql.connector.Error as erro:
            print(f"\n ERRO FATAL DE CONEXAO COM BANCO DE DADOS: {erro}")
            print("\n Produto não encontrado. Tente novamente mais tarde.") 
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

def exibir_catalogo():
    try:
        # Conexão com o banco de dados
        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, categoria, preco_custo, preco_venda, preco_original, preco_promocao, qtd_estq, status
            FROM Produto
            WHERE status = 1
        """)

        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()

        if len(resultados) == 0:
            print("\n Nenhum produto encontrado...")
        else:
            for produto in resultados:
                print(f"""
{'='*140}
{'ID':<5} | {'NOME':<20} | {'CATEGORIA':<15} | {'PREÇO CUSTO':<15} | {'PREÇO VENDA':<15} | {'PREÇO ORIGINAL':<15} | {'PREÇO PROMOÇÃO':<17} | {'ESTOQUE':<10} | {'STATUS':<10}
{'='*140}
{produto[0]:<5} | {produto[1]:<20} | {produto[2]:<15} | R${produto[3]:<15.2f} | R${produto[4]:<15.2f} | R${produto[5]:<15.2f} | R${produto[6]:<17.2f} | {produto[7]:<10} | {produto[8]:<10}
{'='*140}
""")

    #Método para tratar erros de conexão com o banco de dados
    #Segurando que o programa não quebre e informe o usuário sobre o erro
    except mysql.connector.Error as erro:
        print(f"\n ERRO FATAL DE CONEXAO COM BANCO DE DADOS: {erro}")
        print("\n Produto não encontrado. Tente novamente mais tarde.")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()