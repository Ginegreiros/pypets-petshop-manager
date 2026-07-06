
import os
from dotenv import load_dotenv
from conexao import obter_conexao
import mysql.connector

load_dotenv()

def iniciar_db():
    """
    Cria o banco de dados, as tabelas e insere os dados iniciais
    """
    try: 
        # Conecta no MySQL "puro", sem escolher o database
        con_setup = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor_setup = con_setup.cursor()

        # Cria o banco de dados se não existir
        cursor_setup.execute("CREATE DATABASE IF NOT EXISTS py_pets;")
        con_setup.commit()

        cursor_setup.close()
        con_setup.close() # <--- ADICIONE ESTA LINHA AQUI
    
    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
        return # interrompe tude se o servidor MySQL estiver desligado

    try:
        # Usando a conexão de conexão.py
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        # Cria a tabelas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cliente(
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
                ("Maria Silva",   "11999990001", "11111111101"),
                ("João Pereira",  "11999990002", "22222222202"),
                ("Ana Souza",     "11999990003", "33333333303"),
            ]
            cursor.executemany("""
                INSERT INTO Cliente (nome, telefone, cpf)
                VALUES (%s, %s, %s)
            """, clientes_padrao)
        conexao.commit()
    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()
    try:
                # Usando a conexão de conexão.py
        conexao = obter_conexao()
        cursor = conexao.cursor()

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
                ("Rex",     "Cachorro", "Labrador",       1),  # id_cliente = 1 (Maria)
                ("Mimi",    "Gato",     "Persa",          2),  # id_cliente = 2 (João)
                ("Bolinha", "Cachorro", "Poodle",         3)  # id_cliente = 3 (Ana)
            ]
            cursor.executemany("""
                INSERT INTO Pet (nome, especie, raca, id_cliente)
                VALUES (%s, %s, %s, %s)
            """, pets_padrao)
        conexao.commit()

    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()

    try:
        # Usando a conexão de conexão.py
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Produto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                categoria VARCHAR(100) NOT NULL, 
                preco_custo DECIMAL(10,2) NOT NULL,
                preco_venda DECIMAL(10,2) NOT NULL,
                preco_original DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                preco_promocao DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                qtd_estq INT NOT NULL DEFAULT 0,
                status TINYINT(1) NOT NULL DEFAULT 1
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM Produto")
        if cursor.fetchone()[0] == 0:
            produtos_padrao = [
                ("Ração Golden Adult", "Alimentação", 45.00, 89.90, 30),
                ("Shampoo Pet Clean",  "Higiene",     12.00, 28.50, 50),
                ("Coleira Ajustável",  "Acessórios",   8.00, 19.90, 40)
            ]
            cursor.executemany(""" 
                INSERT INTO Produto (nome, categoria, preco_custo, preco_venda, qtd_estq)
                VALUES (%s, %s, %s, %s, %s)
            """, produtos_padrao)
        conexao.commit()

    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()

    try:
        # Usando a conexão de conexão.py
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Servico (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                descricao VARCHAR(150),
                preco DECIMAL(10,2) NOT NULL,
                status TINYINT(1) NOT NULL DEFAULT 1
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM Servico")
        if cursor.fetchone()[0] == 0:
            Servicos_padrao = [
                ("Banho",        "Banho completo com secagem",     35.00),
                ("Tosa",         "Tosa higiênica ou completa",     45.00),
                ("Banho & Tosa", "Combo banho e tosa com desconto",70.00)
            ]
            cursor.executemany("""
                INSERT INTO Servico (nome, descricao, preco)
                VALUES (%s, %s, %s)
            """, Servicos_padrao)
        conexao.commit()

    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()

    try:
        # Usando a conexão de conexão.py
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Agendamento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_hora DATETIME NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'Agendado',
                id_pet INT NOT NULL,
                FOREIGN KEY (id_pet) REFERENCES Pet(id)
            )
        """)
        conexao.commit()

    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()

    try:
        # Usando a conexão de conexão.py
        conexao = obter_conexao()
        cursor = conexao.cursor()        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AgendamentoServico (
                id_agendamento INT NOT NULL,
                id_servico INT NOT NULL,
                preco_cobrado DECIMAL(10,2) NOT NULL, -- Preço do momento do agendamento (histórico)
                PRIMARY KEY (id_agendamento, id_servico),
                FOREIGN KEY (id_agendamento) REFERENCES Agendamento(id) ON DELETE CASCADE,
                FOREIGN KEY (id_servico) REFERENCES Servico(id)
            )
        """)
        conexao.commit()
    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()

    try:
        # Usando a conexão de conexão.py
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Venda (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_venda DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                valor_total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                status TINYINT(1) NOT NULL DEFAULT 1
            )
        """)
        conexao.commit()
    except mysql.connector.Error as erro:
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()

    try:
        # Usando a conexão de conexão.py
        conexao = obter_conexao()
        cursor = conexao.cursor()
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
        print(f" ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()