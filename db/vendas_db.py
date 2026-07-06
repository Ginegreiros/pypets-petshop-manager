
import datetime
import mysql.connector

from conexao import obter_conexao


#lista de produtos disponiveis para venda
def listar_produtos_para_venda():
    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return []

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, preco_venda, qtd_estq, status
            FROM Produto
            WHERE status = 1
            ORDER BY id ASC
        """)

        return cursor.fetchall()

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXAO COM BANCO: {erro}")
        return []
    

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()



def buscar_produto_para_venda(id_produto):
    # Busca o produto antes de colocar no carrinho.
    # Aqui ja filtro apenas produto ativo.
    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return None

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, preco_venda, qtd_estq, status
            FROM Produto
            WHERE id = %s AND status = 1
        """, (id_produto,))

        return cursor.fetchone()

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXAO COM BANCO: {erro}")
        return None

    finally:
        # Fecha tudo para nao deixar conexao aberta.
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()



def finalizar_venda(carrinho):
    # Finaliza a venda de verdade, gravando no banco.
    # Venda, itens e baixa de estoque ficam na mesma transacao.
    conexao = None
    cursor = None

    if len(carrinho) == 0:
        print("ERRO: carrinho vazio.")
        return False

    data_venda = datetime.datetime.now()
    valor_total = sum(item["subtotal"] for item in carrinho)

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return False

        cursor = conexao.cursor()

        # A partir daqui, ou tudo da certo, ou tudo e desfeito.

        # Primeiro registra a venda principal.
        cursor.execute("""
            INSERT INTO Venda (
                data_venda,
                valor_total,
                status
            )
            VALUES (%s, %s, %s)
        """, (
            data_venda,
            valor_total,
            1
        ))

        id_venda = cursor.lastrowid

        for item in carrinho:
            # Confere o produto novamente no banco antes de vender.
            # FOR UPDATE ajuda a evitar conflito de estoque.
            cursor.execute("""
                SELECT nome, preco_venda, qtd_estq, status
                FROM Produto
                WHERE id = %s
                FOR UPDATE
            """, (item["id_produto"],))

            produto = cursor.fetchone()

            if produto is None:
                raise Exception("Produto nao encontrado.")

            nome_produto = produto[0]
            estoque_atual = produto[2]
            status_produto = produto[3]

            if status_produto != 1:
                raise Exception(f"Produto inativo: {nome_produto}")

            if estoque_atual < item["quantidade"]:
                raise Exception(f"Estoque insuficiente para: {nome_produto}")

            # Salva o item da venda com o preco do momento.
            cursor.execute("""
                INSERT INTO ItemVenda (
                    id_venda,
                    id_produto,
                    qtd,
                    preco_unitario
                )
                VALUES (%s, %s, %s, %s)
            """, (
                id_venda,
                item["id_produto"],
                item["quantidade"],
                item["preco_unitario"]
            ))

            # Depois de registrar o item, baixa o estoque.
            cursor.execute("""
                UPDATE Produto
                SET qtd_estq = qtd_estq - %s
                WHERE id = %s
                  AND status = 1
                  AND qtd_estq >= %s
            """, (
                item["quantidade"],
                item["id_produto"],
                item["quantidade"]
            ))

            if cursor.rowcount == 0:
                raise Exception(f"Nao foi possivel atualizar o estoque de: {nome_produto}")

        conexao.commit()
        print("\n*********** VENDA FINALIZADA COM SUCESSO!!! ***********")
        return True

    except mysql.connector.Error as erro:
        # Se o banco falhar, desfaz qualquer coisa feita na venda.
        if conexao and conexao.is_connected():
            conexao.rollback()

        print(f"ERRO FATAL DE CONEXAO COM BANCO: {erro}")
        print("NENHUMA VENDA FOI REGISTRADA!!!")
        return False

    except Exception as erro:
        # Qualquer erro de regra tambem cancela a venda.
        if conexao and conexao.is_connected():
            conexao.rollback()

        print(f"ERRO NA VENDA: {erro}")
        print("NENHUMA VENDA FOI REGISTRADA!!!")
        return False

    finally:
        # Sempre fecha cursor e conexao no final.
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def cancelar_venda(id_venda):
    # Cancela sem apagar do banco.
    # Aqui usamos soft delete mudando o status para 0.
    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return False

        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE Venda
            SET status = 0
            WHERE id = %s AND status = 1
        """, (id_venda,))

        conexao.commit()

        if cursor.rowcount == 0:
            print("ERRO: Venda nao encontrada ou ja cancelada.")
            return False

        print("Venda cancelada com sucesso.")
        return True

    except mysql.connector.Error as erro:
        if conexao and conexao.is_connected():
            conexao.rollback()

        print(f"ERRO FATAL DE CONEXAO COM BANCO: {erro}")
        return False

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()


def listar_vendas():
    # Lista as vendas para conferencia ou para o financeiro usar depois.
    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return []

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, data_venda, valor_total, status
            FROM Venda
            ORDER BY data_venda DESC
        """)

        return cursor.fetchall()

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXAO COM BANCO: {erro}")
        return []

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()