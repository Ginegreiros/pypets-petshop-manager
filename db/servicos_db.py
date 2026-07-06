

from conexao import obter_conexao
import mysql.connector

def listar_servicos():
    """Retorna todos os serviços disponíveis no catálogo"""
   
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
            SELECT id, nome, descricao, preco
            FROM Servico
            WHERE status = 1
        """)

        #Busca todas as linhas que o banco retornou e guarda como uma lista de tuplas em servicos.
        servicos = cursor.fetchall()

        if not servicos:
            print("Nenhum serviço disponível no momento.")
            #aqui retorna uma lista vazia para indicar que não há serviços disponíveis
            #objetivo é mostrar ao usuário que não há serviços disponíveis
            #mas ainda assim retornar uma lista vazia para que o programa continue funcionando sem erros
            return []
        
        print("\n ====== Serviços Disponíveis ====== ")
        for s in servicos:
            print(f"ID: {s[0]}, Nome: {s[1]}, Descrição: {s[2]}, Preço: R${s[3]:.2f}")

        return servicos
    
    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXAO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def servico_id():
    """Retorna um serviço específico pelo ID"""
    try:
        id_servico = int(input("Digite o ID do serviço que deseja acessar: "))
    except ValueError:
        print("ERRO: ID DEVE SER NÚMERO!!!")
        return

    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()

        if conexao is None:
            print("ERRO: nao foi possivel conectar ao banco.")
            return

        cursor = conexao.cursor()
        cursor.execute("""
            SELECT id, nome, preco
            FROM Servico
            WHERE id = %s
            AND status = 1
        """, (id_servico,))

        #Guarda APENAS uma linha que o banco retornou e armazena em uma tupla em servicos.
        servico = cursor.fetchone()

        if not servico:
            print("Serviço não encontrado ou indisponível.")
            return None

        #aqui retorna id, nome e preço do serviço encontrado
        return servico

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXAO: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()