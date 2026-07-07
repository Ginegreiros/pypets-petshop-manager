
#db/ financeiro_bd.py 

import mysql.connector
from conexao import obter_conexao

def buscar_ranking_produtos():

    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()
        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return []
        
        cursor = conexao.cursor()

        query = """
        SELECT 
            P.nome,
            SUM(iv.qtd) AS total_vendido,
            SUM(iv.qtd * iv.preco_unitario) AS faturamento
        FROM ItemVenda iv
        INNER JOIN Produto p
            ON p.id = iv.id_produto
        INNER JOIN Venda v
            ON v.id = iv.id_venda
        WHERE v.status = 1
        GROUP BY P.id, p.nome
        ORDER BY total_vendido DESC
            
        """

        cursor.execute(query)

        return cursor.fetchall()
    
    except Exception as erro:

        print(f"Erro ao buscar ranking: {erro}")
        return []
    
    finally:
        if cursor:
            cursor.close()
            
        if conexao and conexao.is_connected():
            conexao.close()


def buscar_ranking_servicos():

    conexao = None
    cursor = None

    try:

        conexao = obter_conexao()
        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return []
        
        cursor = conexao.cursor()

        query = """
        SELECT 
            s.nome,
            COUNT(*) AS total_realizado,
            SUM(ag.preco_cobrado) AS faturamento

        FROM AgendamentoServico ag

        INNER JOIN Servico s
            ON s.id = ag.id_servico
        
        GROUP BY s.id, s.nome
        ORDER BY total_realizado DESC

        """
        cursor.execute(query)
        return cursor.fetchall()

    except Exception as erro:
        print(f"Erro ao buscar ranking de serviços: {erro}")
        return []
    
    finally:
        if cursor:
            cursor.close()
            
        if conexao and conexao.is_connected():
            conexao.close()

def buscar_dados_bi():

    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()
        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return {}
        cursor = conexao.cursor()

        dados = {}

        cursor.execute("""
            SELECT COUNT(*)
            FROM Venda
            WHERE status = 1
        """)

        dados["total_vendas"] = cursor.fetchone()[0]


        cursor.execute("""
            SELECT COALESCE(SUM(iv.qtd * iv.preco_unitario), 0)
            FROM ItemVenda iv
            INNER JOIN Venda v ON v.id = iv.id_venda
            WHERE v.status = 1
        """)
        dados["faturamento"] = cursor.fetchone()[0] or 0.0

        cursor.execute("""
            SELECT COALESCE(SUM((p.preco_venda - p.preco_custo) * iv.qtd), 0)
            FROM ItemVenda iv
            INNER JOIN Produto p ON p.id =iv.id_produto
            INNER JOIN Venda v ON v.id = iv.id_venda
            WHERE v.status = 1
        """)
        dados["margem_lucro"] = cursor.fetchone()[0] or 0.0


        return dados
    
    except Exception as erro:
        print(f"Erro ao buscar dados BI: {erro}")
        return {}
    
    finally:
        if cursor:
            cursor.close()
            
        if conexao and conexao.is_connected():
            conexao.close()

    

def buscar_nota_fiscal(id_venda):

    conexao = None
    cursor = None

    try:

        conexao = obter_conexao()
        
        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return None

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                v.id,
                v.data_venda,
                v.valor_total
            FROM Venda v
            WHERE v.id = %s
            AND v.status = 1
        """, (id_venda,))

        venda = cursor.fetchone()

        if not venda:
            return None
        
        cursor.execute("""

            SELECT
                p.nome,
                iv.qtd,
                iv.preco_unitario
            FROM ItemVenda iv
            INNER JOIN Produto p
                ON p.id = iv.id_produto
            WHERE iv.id_venda = %s

        """, (id_venda,))

        itens = cursor.fetchall()

        return {
            "venda": venda,
            "itens": itens
        }
    
    except Exception as erro:
        print(f"Erro ao buscar nota fiscal: {erro}")
        return None
    
    finally:
        if cursor:
            cursor.close()
            
        if conexao and conexao.is_connected():
            conexao.close()


def buscar_nota_fiscal_servico(id_agendamento):
    """
    Busca os dados de um agendamento (cliente, pet, data) e os serviços cobrados nele, para montar a nota fiscal de serviços.
    Equivalente à buscar_nota_fiscal(), só que para Agendamento em vez de Venda.
    """

    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return None

        cursor = conexao.cursor()

        # 1) Busca os dados principais do agendamento (cabeçalho da nota)
        #    Só busca se o status for 'Concluido' — não emite nota de agendamento
        #    cancelado ou ainda pendente.
        cursor.execute("""
            SELECT
                agendamento.id,
                agendamento.data_hora,
                pet.nome,
                cliente.nome
            FROM agendamento
            INNER JOIN pet ON agendamento.id_pet = pet.id
            INNER JOIN cliente ON pet.id_cliente = cliente.id
            WHERE agendamento.id = %s
            AND agendamento.status = 'Concluido'
        """, (id_agendamento,))

        agendamento = cursor.fetchone()

        if not agendamento:
            return None

        # 2) Busca os serviços cobrados nesse agendamento (itens da nota)
        cursor.execute("""
            SELECT
                servico.nome,
                agendamentoservico.preco_cobrado
            FROM agendamentoservico
            INNER JOIN servico ON agendamentoservico.id_servico = servico.id
            WHERE agendamentoservico.id_agendamento = %s
        """, (id_agendamento,))

        itens = cursor.fetchall()

        return {
            "agendamento": agendamento,
            "itens": itens
        }

    except Exception as erro:
        print(f"Erro ao buscar nota fiscal de serviço: {erro}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()

def buscar_promocoes():

    conexao = None
    cursor = None

    try:

        conexao = obter_conexao()
        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return []
        cursor = conexao.cursor()
        
        query = """

        SELECT 
            id,
            nome,
            preco_original,
            preco_promocao

        FROM Produto

        WHERE status = 1
        AND preco_promocao > 0
        AND preco_promocao < preco_original

        ORDER BY nome

        """

        cursor.execute(query)

        return cursor.fetchall()
    
    except Exception as erro:

        print(f"Erro ao buscar promoções: {erro}")
        return []
    
    finally:
        if cursor:
            cursor.close()
            
        if conexao and conexao.is_connected():
            conexao.close()



def buscar_total_servicos():

    conexao = None
    cursor = None

    try:

        conexao = obter_conexao()
        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return 0
        
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM AgendamentoServico
        """)

        return cursor.fetchone()[0]
    
    except Exception as erro:
        print(f"Erro ao buscar total de serviços: {erro}")
        return 0
    
    finally:
        if cursor:
            cursor.close()
            
        if conexao and conexao.is_connected():
            conexao.close()


def aplicar_promocao(id_produto, percentual_desconto):

    conexao = None
    cursor = None

    if percentual_desconto <= 0 or percentual_desconto >= 100:
        print("ERRO: desconto deve ser maior que 0 e menor que 100.")
        return False

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return False

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT nome, preco_venda, preco_original, preco_promocao
            FROM Produto
            WHERE id = %s AND status = 1
        """, (id_produto,))

        produto = cursor.fetchone()

        if produto is None:
            print("ERRO: produto nao encontrado ou inativo.")
            return False

        nome = produto[0]
        preco_venda = produto[1]
        preco_original = produto[2]
        preco_promocao = produto[3]

        if preco_promocao > 0:
            print("ERRO: produto ja esta em promocao.")
            return False

        if preco_original == 0:
            preco_original = preco_venda

        novo_preco = preco_original - (preco_original * percentual_desconto / 100)

        cursor.execute("""
            UPDATE Produto
            SET preco_original = %s,
                preco_promocao = %s,
                preco_venda = %s
            WHERE id = %s
        """, (preco_original, novo_preco, novo_preco, id_produto))

        conexao.commit()
        print(f"Promocao aplicada em '{nome}'. Novo preco: R$ {novo_preco:.2f}")
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


def remover_promocao(id_produto):

    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return False

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT nome, preco_original, preco_promocao
            FROM Produto
            WHERE id = %s AND status = 1
        """, (id_produto,))

        produto = cursor.fetchone()

        if produto is None:
            print("ERRO: produto nao encontrado ou inativo.")
            return False

        nome = produto[0]
        preco_original = produto[1]
        preco_promocao = produto[2]

        if preco_promocao <= 0:
            print("ERRO: produto nao esta em promocao.")
            return False

        cursor.execute("""
            UPDATE Produto
            SET preco_venda = %s,
                preco_promocao = 0.00,
                preco_original = 0.00
            WHERE id = %s
        """, (preco_original, id_produto))

        conexao.commit()
        print(f"Promocao removida de '{nome}'. Preco original restaurado.")
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