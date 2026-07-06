
import os 
from dotenv import load_dotenv
from conexao import obter_conexao

import mysql.connector

load_dotenv()

def _criar_banco_se_nao_existir():

    """Conecta no MySQL 'puro' (sem escolher database) e cria o py_pets se não existir."""


    try: 

        con_setup = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor_setup = con_setup.cursor()
        cursor_setup.execute("CREATE DATABASE IF NOT EXISTS PY_PETS;")
        con_setup.commit()
        cursor_setup.close()
        con_setup.close()

    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
        raise # repassa o erro para o iniciar_db() saber que precisa parar

def iniciar_db():

    """
    Cria o banco de dados, as tabelas e insere os dados iniciais.
    """
    try:
        _criar_banco_se_nao_existir()

    except mysql.connector.Error:
        return # interrompe tudo se o servidor MySQL estiver desligado

    try: 
        #uma única conexão para todas as tabelas
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # ===== Cliente =====

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cliente (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                telefone VARCHAR(11) NOT NULL,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                status TINYINT(1) NOT NULL DEFAULT 1
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM Cliente")

        if cursor.fetchone()[0] == 0:
            clientes_padrao = [
                ("João Silva", "11999999999", "12345678901"),
                ("Maria Souza", "21988888888", "23456789012"),
                ("Pedro Oliveira", "31977777777", "34567890123"),
                ("Ana Santos", "41966666666", "45678901234"),
                ("Lucas Costa", "51955555555", "56789012345")
            ]

            cursor.executemany("""
                INSERT INTO Cliente (nome, telefone, cpf)
                VALUES (%s, %s, %s)
            """, clientes_padrao)

        # ===== Pet =====

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pet(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                especie VARCHAR(50) NOT NULL,
                raca VARCHAR(50) NOT NULL,
                id_cliente INT NOT NULL,
                status TINYINT(1) NOT NULL DEFAULT 1,
                FOREIGN KEY (id_cliente) REFERENCES Cliente(id)   
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM Pet")
        if cursor.fetchone()[0] == 0:
            pets_padrao = [
                ("Rex", "Cachorro", "Labrador", 1),
                ("Mia", "Gato", "Siamês", 2),
                ("Buddy", "Cachorro", "Golden Retriever", 3),
                ("Luna", "Gato", "Persa", 4),
                ("Max", "Cachorro", "Bulldog Francês", 5)
            ]

            cursor.executemany("""
                INSERT INTO Pet (nome, especie, raca, id_cliente)
                VALUES (%s, %s, %s, %s)
            """, pets_padrao)

        # ===== Produto =====

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Produto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                preco_custo DECIMAL(10, 2) NOT NULL,
                preco_venda DECIMAL(10, 2) NOT NULL,
                preco_original DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                preco_promocao DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                qtd_estq INT NOT NULL DEFAULT 0,
                status TINYINT(1) NOT NULL DEFAULT 1
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM Produto")
        if cursor.fetchone()[0] == 0:
            produtos_padrao = [
                ("Ração Golden Adult", "Alimentação", 45.00, 89.90, 30),
                ("Shampoo Pet Clean",  "Higiene",     12.00, 28.50, 50),
                ("Coleira Ajustável",  "Acessórios",   8.00, 19.90, 40),
            ]
            cursor.executemany("""
                INSERT INTO Produto (nome, categoria, preco_custo, preco_venda, qtd_estq)
                VALUES (%s, %s, %s, %s, %s)
            """, produtos_padrao)

        # ==== Servico =====

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Servico (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                descricao VARCHAR(150),
                preco DECIMAL(10, 2) NOT NULL,
                status TINYINT(1) NOT NULL DEFAULT 1
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM Servico")
        if cursor.fetchone()[0] == 0:
            servicos_padrao = [
                ("Banho",        "Banho completo com secagem",      35.00),
                ("Tosa",         "Tosa higiênica ou completa",      45.00),
                ("Banho & Tosa", "Combo banho e tosa com desconto", 70.00),
            ]
            cursor.executemany("""
                INSERT INTO Servico (nome, descricao, preco)
                VALUES (%s, %s, %s)
            """, servicos_padrao)

        # === agendamento ===

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Agendamento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_hora DATETIME NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'Agendado',
                id_pet INT NOT NULL,
                FOREIGN KEY (id_pet) REFERENCES Pet(id),
            )

        """)

        # ===== agendamentoServico =====

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AgendamentoServico (
                id_agendamento INT NOT NULL,
                id_servico INT NOT NULL,
                preco_cobrado DECIMAL(10,2) NOT NULL,
                PRIMARY KEY (id_agendamento, id_servico),
                FOREIGN KEY (id_agendamento) REFERENCES Agendamento(id) ON DELETE CASCADE,
                FOREIGN KEY (id_servico) REFERENCES Servico(id)
            )
        """)

        # --- Venda ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Venda (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_venda DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                valor_total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                status TINYINT(1) NOT NULL DEFAULT 1
            )
        """)

        # --- ItemVenda ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ItemVenda (
                id_venda INT NOT NULL,
                id_produto INT NOT NULL,
                qtd INT NOT NULL,
                preco_unitario DECIMAL(10,2) NOT NULL,
                PRIMARY KEY (id_venda, id_produto),
                FOREIGN KEY (id_venda) REFERENCES Venda(id) ON DELETE CASCADE,
                FOREIGN KEY (id_produto) REFERENCES Produto(id)
            )
        """)

        conexao.commit()

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()



