
import mysql.connector
from conexao import obter_conexao
from relatorios.filtros import exibir_catalogo

def listar_produtos_simples(status_prod=1):

    """
    Exibe uma lista curta (ID, Nome, Preço, Quantidade) para auxiliar na escolha de IDs nos menus.
    """

    conexao = None
    cursor = None

    try: 
        conexao = obter_conexao()

        if conexao is None:
            return False
        cursor = conexao.cursor()

        #Filtra pelo status passado como parâmetro ( 1= ativo, 0=inativo)
        cursor.execute("""

            SELECT id, nome, preco_venda, qtd_estq
            FROM Produto
            WHERE status = %s
            ORDER BY id ASC
        """, (status_prod,))

        produtos = cursor.fetchall()

        if not produtos:
            print("\nERRO: Nenhum produto encontrado no sistema.")
            return False
        
        print("\n" + "="*40)
        print(f"{'ID':<5} {'NOME':<20} {'PREÇO':>10} {'ESTOQUE':>8}")
        print("="*40)

        for produto in produtos:
            print(f"{produto[0]:<5} {produto[1][:20]:<20} R${produto[2]:.2f} {produto[3]:>8}")
        print("="*40)
        return True
    
    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXAO COM BANCO:{erro}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


def alt_infos():

    print("\n========== ALTERAR DADOS CADASTRAIS ==========")

    listar_produtos_simples(1)

    try:
        id_produto = int(input("Digite o ID do produto que deseja alterar informações: "))
    except ValueError:
        print("ERRO: O ID DEVE SER UM NÚMERO!!!")
        return

    #Inicia as duas variáveis como None antes de tentar qualquer coisa.
    #Isso é uma precaução — garante que elas existem no escopo da função, 
    #então o bloco finally consegue verificar se foram criadas sem dar NameError.
    conexao = None
    cursor = None

    #Método de segurança para validação de conexão com o banco de dados.
    try:
        conexao = obter_conexao()

        #Pode ser considerado método de segurança também
        #Se obter_conexao() falhou silenciosamente e retornou None, isso impede que o código continue
        #Dessa forma o código não quebra caso a conexão falhe
        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return

        cursor = conexao.cursor()


        cursor.execute("""
            SELECT nome, preco_venda, qtd_estq, categoria
            FROM Produto
            WHERE id = %s
        """, (id_produto,))
        produto = cursor.fetchone()

        if not produto:
            print("ERRO: ID INVÁLIDO.")
            return
        print(f"\n Alterando dados de '{produto[0]}', preço atual: {produto[1]}, quantidade atual: {produto[2]}")
        print("\n(Caso não queira prosseguir pressione tecla Enter.)")

        #Definindo nomes as variáveis que substituirão valores.
        new_name = input(f"\nAlterar nome de '{produto[0]}' para: ").strip().lower() or produto[0]
        price_str = input(f"\nAltere o preço de R${produto[1]} para: ").strip().lower()
        qtd_str = input(f"\nAtualize a quantidade de {produto[2]} para: ").strip().lower()
        new_categ = input(f"\nAtualize a categoria de {produto[3]} para: ").strip().lower() or produto[3]

        #Abaixo temos um método de segurança para cada variável que armazena valor numérico

        try:
            new_price = float(price_str) if price_str else produto[1]
        except ValueError:
            print("ERRO: VALOR PRECISA SER NUMÉRICO!")
            return
        try:
            new_qtd = int(qtd_str) if qtd_str else produto[2]
        except ValueError:
            print(f"\nERRO: QUANTIDADE DEVE SER NÚMERO.")
            return

        if new_price < 0:
            print("ERRO: PREÇO NÃO PODE SER NEGATIVO!!!")
            return
        if new_qtd < 0:
            print("ERRO: QUANTIDADE NÃO PODE SER NEGATIVA!!!")
            return
        cursor.execute("""
            UPDATE Produto
            SET nome = %s,
                preco_venda = %s,
                qtd_estq = %s,
                categoria = %s
            WHERE id = %s
        """, (new_name, new_price, new_qtd, new_categ, id_produto))

        conexao.commit()
        print("\n***********DADOS ATUALIZADOS COM SUCESSO!!!***********")

    except mysql.connector.Error as erro:
        if conexao and conexao.is_connected():
            conexao.rollback()
        print(f" ERRO FATAL DE CONEXAO COM BANCO:{erro} ")
        print("NENHUM DADO FOI ALTERADO!!!")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def desativ_prod():

    while True:

        print("\n REMOVENDO PRODUTOS DO CATÁLOGO")

        listar_produtos_simples(1)

        try:
            id_produto = int(input("Digite o ID do produto que deseja desativar: "))
        except ValueError:
            print("ERRO: O ID DEVE SER NÚMERO!!!")
            return

        if id_produto == 0:
            print("\nRetornando ao menu principal...")
            break

        conexao = None
        cursor = None

        try:
            conexao = obter_conexao()
            if conexao is None:
                print("ERRO: nao foi possivel conectar ao banco.")
                return

            cursor = conexao.cursor()
            cursor.execute("""
                SELECT nome
                FROM Produto
                WHERE id = %s AND status = 1
            """, (id_produto,))
            produto = cursor.fetchone()

            if not produto:
                print("\nERRO: Produto não encontrado ou já desativado.")
                return
            print("Digite 0 para cancelar e voltar ao menu principal.")
            confirmar = input(f"\nTem certeza que deseja DESATIVAR o produto '{produto[0]}'? (s/n): ").strip().lower()

            if confirmar == '0':
                break
            elif confirmar == 's':
                cursor.execute("""
                    UPDATE Produto
                    SET status = 0
                    WHERE id = %s
                """, (id_produto,))
                conexao.commit()
                print(f"Exclusão de '{produto[0]}' realizada com sucesso!!!")
                break
            else:
                continue

        except mysql.connector.Error as erro:
            if conexao and conexao.is_connected():
                conexao.rollback()
            print(f" ERRO FATAL DE CONEXAO COM BANCO:{erro}  ")
            print("NENHUM DADO FOI ALTERADO!!!")
        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

def ativ_prod():

    while True:

        listar_produtos_simples(0)
        
        print("\n ATIVANDO PRODUTOS NO CATÁLOGO")
        try:
            id_produto = int(input("Digite o ID do produto que deseja ativar: "))
        except ValueError:
            print("ERRO: O ID DEVE SER NÚMERO!!!")
            return

        if id_produto == 0:
            print("\nRetornando ao menu principal...")
            break

        conexao = None
        cursor = None
        try:
            conexao = obter_conexao()

            if conexao is None:
                print("ERRO: nao foi possivel conectar ao banco.")
                return

            cursor = conexao.cursor()
            cursor.execute("""
                SELECT nome
                FROM Produto
                WHERE id = %s AND status = 0
            """, (id_produto,))
            produto = cursor.fetchone()

            if not produto:
                print("\nERRO: Produto não encontrado ou já está ativo.")
                return

            print("Digite 0 para cancelar e voltar ao menu principal.")
            confirmar = input(f"\nTem certeza que deseja ATIVAR o produto '{produto[0]}'? (s/n): ").strip().lower()

            if confirmar == '0':
                break
            elif confirmar == 's':
                cursor.execute("""
                    UPDATE Produto
                    SET status = 1
                    WHERE id = %s
                """, (id_produto,))
                conexao.commit()
                print(f"Ativação de '{produto[0]}' realizada com sucesso!!!")
                break
            else:
                continue

        except mysql.connector.Error as erro:
            if conexao and conexao.is_connected():
                conexao.rollback()
            print(f" ERRO FATAL DE CONEXAO COM BANCO:{erro} ")
            print("NENHUM DADO FOI ALTERADO!!!")
        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

def repor_lote(qtd_add, *ids_alvo):
    if len(ids_alvo) == 0:
        print("\nERRO: Digite pelo menos um ID de produto ativo")
        return

    if qtd_add <= 0:
        print("\nERRO: QUANTIDADE DEVE SER MAIOR QUE ZERO!!!")
        return

    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return

        cursor = conexao.cursor()

        print(f"\nIniciando reposição de +{qtd_add} unidades para IDs selecionados... ")

        for id_produto in ids_alvo:
            cursor.execute("""
                SELECT nome
                FROM Produto
                WHERE id = %s AND status = 1
            """, (id_produto,))
            resultado = cursor.fetchone()

            if not resultado:
                print(f"\nERRO: Produto com ID {id_produto} não existe no sistema.")
                continue

            nome_prod = resultado[0]

            cursor.execute("""
                UPDATE Produto
                SET qtd_estq = qtd_estq + %s
                WHERE id = %s
            """, (qtd_add, id_produto))

            print(f"Foram adicionados +{qtd_add} do(s) seguinte produto(s): {nome_prod}")

            conexao.commit()

    except mysql.connector.Error as erro:
        if conexao and conexao.is_connected():
            conexao.rollback()
        print(f" ERRO FATAL DE CONEXAO COM BANCO:{erro} ")
        print("NENHUM DADO FOI ALTERADO!!!")

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def cad_prod():
    print("\n ====== Cadastro de Produto ====== ")

    novo_nome = input("Digite o nome do produto: ").strip()
    nova_categ = input("Digite a categoria do produto: ").strip()

    #Método para validar se o usuário digitou apenas números para o preço e quantidade
    try:
        novo_custo = float(input("Digite o custo do produto: "))
    except ValueError:
        print("\n ERRO: PREÇO DE CUSTO -> DIGITE NÚMEROS E PONTO NO LUGAR DE VÍRGULA")  
        return
    try:
        novo_preco = float(input("Digite o preço do produto: "))
    except ValueError:
        print("\n ERRO: VALOR DE PRODUTO -> DIGITE NÚMEROS E PONTO NO LUGAR DE VÍRGULA") 
        return 
    
    try:
        nova_qtd = int(input("Digite a quantidade do produto: "))
    except ValueError:
        print("\n ERRO: QUANTIDADE -> DIGITE NÚMEROS E PONTO NO LUGAR DE VÍRGULA") 
        return


    try:
        # Conexão com o banco de dados
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return
        
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO Produto (nome, categoria, preco_custo, preco_venda, qtd_estq)
            VALUES (%s, %s, %s, %s, %s)
        """, (novo_nome, nova_categ, novo_custo, novo_preco, nova_qtd))
        
        #Salvando as alterações no banco de dados
        conexao.commit()
        print(f"\n Produto '{novo_nome}' cadastrado com sucesso!")

    except mysql.connector.Error as erro:
        if conexao and conexao.is_connected():
            conexao.rollback()

        print(f"\nERRO FATAL DE CONEXAO COM BANCO DE DADOS: {erro}")
        print("NENHUM PRODUTO FOI CADASTRADO...")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()