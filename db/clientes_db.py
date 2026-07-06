
from conexao import obter_conexao
import mysql.connector

def list_client():
    """
    mostra os clientes ativos e desativados em listas separadas.
    """
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        #Busca e mostra clientes ativos (status = 1)
        cursor.execute("SELECT id, nome, telefone, cpf FROM cliente WHERE status = 1")
        ativos = cursor.fetchall()
        
        print("\n--- CLIENTES ATIVOS NO SISTEMA ---")
        if not ativos:
            print("Nenhum cliente ativo encontrado.")
        else:
            for cliente in ativos:
                print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Tel: {cliente[2]} | CPF: {cliente[3]}")
        print("---------------------------------")

        #Busca e mostra clientes desativados (status = 0)
        cursor.execute("SELECT id, nome, telefone, cpf FROM cliente WHERE status = 0")
        desativados = cursor.fetchall()
        
        print("\n--- CLIENTES DESATIVADOS NO SISTEMA ---")
        if not desativados:
            print("Nenhum cliente desativado encontrado.")
        else:
            for cliente in desativados:
                print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Tel: {cliente[2]} | CPF: {cliente[3]}")
        print("---------------------------------")
        return True

    except mysql.connector.Error as erro:
        print(f"Erro ao listar clientes: {erro}")
        return False
        
    finally:
        # Garante o fechamento do banco
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def buscar_cliente_cpf(cpf):
    """
    Busca um cliente ativo pelo CPF e retorna o ID se encontrar.
    """
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        # Procura o ID do cliente usando o CPF informado e que esteja ativo (status = 1)
        cursor.execute("SELECT id FROM cliente WHERE cpf = %s AND status = 1", (cpf,))
        #Pega a primeira linha que o banco encontrar
        resultado = cursor.fetchone()
        #Se encontrar, devolve o ID do cliente
        if resultado:
            return resultado[0]
        else:
            print("Cliente não encontrado ou está inativo.")
            return 

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
        return 
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def cad_cliente(): 
    """
    Cadastra um novo cliente no banco de dados.
    """
    print("\n------ CADASTRAR NOVO CLIENTE ----------")
 
    cpf = input("Digite o CPF do cliente (somente números): ").strip()
    if not cpf:
        print("ERRO: CPF é obrigatório.")
        return

    if not cpf.isdigit():
        print("ERRO: CPF deve conter apenas números.")
        return

    if len(cpf) != 11:
        print("ERRO: CPF deve conter exatamente 11 dígitos.")
        return
    
    # Validação do nome
    nome = input("Digite o nome do cliente: ").strip()
    if not nome:
        print("ERRO: Nome é obrigatório.")
        return
        
    if any(caractere.isdigit() for caractere in nome):
        print("ERRO: Nome não pode conter números.")
        return

    # 3. Validação do telefone
    telefone = input("Digite o telefone do cliente (somente números): ").strip()
    if not telefone:
        print("ERRO: Telefone é obrigatório.")
        return
        
    if not telefone.isdigit(): # Se tiver letras ou símbolos, entra aqui
        print("ERRO: Telefone deve conter apenas números.")
        return
    
    if len(telefone) != 11:
        print("ERRO: telefone deve conter exatamente 11 dígitos.")
        return

    #Bloco Banco de Dados
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Verifica se o CPF já existe no bd
        cursor.execute("SELECT cpf FROM Cliente WHERE cpf = %s", (cpf,))
        if cursor.fetchone():
            print(f"ERRO: CPF '{cpf}' já está cadastrado.")
            return
        #Insere o novo cliente 
        cursor.execute(
            "INSERT INTO Cliente (cpf, nome, telefone) VALUES (%s, %s, %s)", 
            (cpf, nome, telefone)
        )
        
        conexao.commit() #Salva as alterações definitivas no banco
        print(f"Cliente '{nome}' salvo com sucesso.")

    except mysql.connector.Error as erro:
        if 'conexao' in locals():
            conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")
        print("Valor não alterado.")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def alt_cliente():
    """
    Altera os dados de um cliente existente usando o ID.
    """
    print("\n------ ALTERAR DADOS DO CLIENTE ----------")
    list_client()
    
    #Validação ID CLIENTE
    try:
        id_input = input("Digite o ID do cliente que deseja alterar: ").strip()
        if not id_input:
            print("ERRO: ID do cliente é obrigatório.")
            return 
        id_cliente = int(id_input)
    except ValueError:
        print("ERRO: ID do cliente deve ser um número.")
        return
    
    
    #BLOCO DO BANCO DE DADOS: Buscar dados atuais
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Busca o nome e telefone atuais do cliente
        cursor.execute(
            "SELECT nome, telefone FROM cliente WHERE id = %s AND status = 1",
            (id_cliente,),
        )
        cliente_atual = cursor.fetchone()
        
        if not cliente_atual:
            print("ERRO: Cliente não encontrado ou está desativado.")
            return
        
        nome_atual = cliente_atual[0]
        telefone_atual = cliente_atual[1]

        print(f"\nDados atuais -> Nome: {nome_atual} | Tel: {telefone_atual}")
        print("(Deixe em branco e pressione Enter para MANTER o dado atual)\n")
    
        #Validação nome
        novo_nome = input("Digite o novo nome do cliente: ").strip().lower()
        if not novo_nome:
            novo_nome = nome_atual  # Mantém o nome atual se o usuário não digitar nada
        else:
            if any(caractere.isdigit() for caractere in novo_nome):
                print("ERRO: Nome não pode conter números.")
                return
    
        #Validação telefone
        novo_telefone = input("Digite o novo telefone do cliente: ").strip()
        if not novo_telefone:
            novo_telefone = telefone_atual #Mantém o atual se der enter
        try:
            int(novo_telefone)  # Verifica se o telefone é numérico
        except ValueError:
            print("ERRO: Telefone deve conter apenas números.")
            return
        if len(novo_telefone) != 11:
            print("ERRO: telefone deve conter exatamente 11 dígitos.")
            return
            
        # 3. BLOCO DO BANCO DE DADOS: Atualizar dados
        cursor.execute(
            "UPDATE cliente SET nome = %s, telefone = %s WHERE id = %s", (novo_nome, novo_telefone, id_cliente))
        conexao.commit()
        print(f"Dados do cliente ID {id_cliente} alterados com sucesso.")

    except mysql.connector.Error as erro:
        if 'conexao' in locals():
            conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def desat_cliente():
    """
    Desativa um cliente existente usando o ID
    """
    print("\n------DESATIVAR UM CLIENTE----------")
    list_client()
    #Validação do cliente 
    try:
        id_input = input("Digite o ID do cliente que deseja desativar: ").strip()
        if not id_input:
            print("ERRO: ID do cliente é obrigatório.")
            return
        id_cliente = int(id_input)  # Se o usuário digitar letras, pula para o ValueError
    except ValueError:
        print("ERRO: ID do cliente deve ser um número válido.")
        return

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        #Buscamos o 'nome' do cliente que está ATIVO (status = 1) para exibir na mensagem de confirmação
        cursor.execute("SELECT nome FROM cliente WHERE id = %s  AND status = 1", (id_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("ERRO: Cliente não encontrado ou já está desativado.")
            return
        
        # Solicita confirmação do usuário antes de desativar o cliente
        confirmacao = input(f"Tem certeza que deseja DESATIVAR o cliente '{cliente[0]}' (ID{id_cliente})? (s/n): ").strip().upper()

        if confirmacao != 'S':
            print("Operação cancelada pelo usuário.")
            return
        
        cursor.execute("UPDATE cliente SET status = 0 WHERE id = %s", (id_cliente,))
        conexao.commit()
        print(f"Cliente ID {id_cliente} desativado com sucesso.")
    
    except mysql.connector.Error as erro:
        if 'conexao' in locals():
            conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def ativar_cliente():
    """
    Ativa um cliente desativado usando o ID
    """
    print("\n------ATIVAR UM CLIENTE----------")
    list_client()
    #Validação do cliente 
    try:
        id_input = input("Digite o ID do cliente que deseja ativar: ").strip()
        if not id_input:
            print("ERRO: ID do cliente é obrigatório.")
            return
        id_cliente = int(id_input)  # Se o usuário digitar letras, pula para o ValueError
    except ValueError:
        print("ERRO: ID do cliente deve ser um número válido.")
        return
    
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        #Procura pelo cliente que está DESATIVADO (status = 0) busca o 'nome' do cliente para exibir na mensagem de confirmação
        cursor.execute("SELECT nome FROM cliente WHERE id = %s AND status = 0", (id_cliente,))
        cliente = cursor.fetchone()
        
        #Se a busca não encontrou, a variável fica vazia e o sistema barra
        if not cliente:
            print("ERRO: Cliente não encontrado ou já está ativo.")
            return
        
        #Solicita confirmação do usuário antes de ativar o cliente
        confirmacao = input(f"Tem certeza que deseja ATIVAR o cliente '{cliente[0]}' (ID{id_cliente})? (s/n): ").strip().upper()

        if confirmacao != 'S':
            print("Operação cancelada pelo usuário.")
            return

        #Atualiza o status do cliente para ativo (status = 1)
        cursor.execute("UPDATE cliente SET status = 1 WHERE id = %s", (id_cliente,))
        conexao.commit()
        print(f"Cliente ID {id_cliente} ativado com sucesso.")

    except mysql.connector.Error as erro:
        if 'conexao' in locals():
            conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()