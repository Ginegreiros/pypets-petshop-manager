
import mysql.connector
from conexao import obter_conexao
#Importamos a função para validar o cliente
from db.clientes_db import buscar_cliente_cpf

def cad_pet():
    """
    Cadastra um novo pet associadondo-o a um CPF de tutor válido
    """
    print("\n-----CADASTRAR NOVO PET-----")

# Validação Pré-cadastro (CPF DO TUTOR)
    cpf_cliente = input("Digite o CPF do Tutor (apenas números): ").strip()
    if not cpf_cliente:
        print("ERRO: O CPF do tutor é obrigatório.")
        return
    try:
        int(cpf_cliente) # Valida se o CPF contém apenas números
    except ValueError:
        print("ERRO: O CPF deve conter apenas valores numéricos válidos.")
        return
# vai até o banco de dados procurar se existe um cliente ativo com esse CPF e traz o número do ID dele de volta.
    id_cliente = buscar_cliente_cpf(cpf_cliente)

    if not id_cliente:
        print("\n[ERRO] Cliente não cadastrado ou desativado. Cadastre o cliente primeiro")
        print("(Menu Cadastro > opcao 2) antes de cadastrar o pet.")
        return 
    #Dados do pet
    nome = input("Digite o nome do Pet: ").strip().lower()
    if not nome:
        print("ERRO: Nome do pet é obrigatório.")
        return
    # vai de caractere por caractere para verificar se não tem nenhum número, se achar o any aciona o if
    if any(caractere.isdigit() for caractere in nome):
        print("ERRO: Nome do pet não pode conter números.")
        return
    especie = input("Digite a espécie do pet (ex: Cachorro, Gato): ").strip().lower()
    if not especie:
        print("ERRO: Espécie do pet é obrigatória.")
        return
    if any(caractere.isdigit() for caractere in especie):
        print("ERRO: A espécie não pode conter números.")
        return
    raca = input("Digite a raça do pet (ou pressione Enter para assumir 'SRD'): ").strip().lower()
    #Se o usuário der Enter sem digitar nada, assume srd (sem raça definida)
    if not raca:
        raca = "srd"
    elif any(caractere.isdigit() for caractere in raca):
        print("ERRO: A raça não pode conter números.")
        return
# Se passar pela validação, insere o pet no banco de dados
    try:
        conexao = obter_conexao()
        if not conexao:
            return
        cursor = conexao.cursor()

# Insere o pet usando o id_cliente encontrado na validação
        cursor.execute("INSERT INTO Pet (nome, especie, raca, id_cliente) VALUES (%s, %s, %s, %s)", 
        (nome, especie, raca, id_cliente))
        conexao.commit()
        print(f" Pet '{nome}' cadastrado com sucesso!!")

    except mysql.connector.Error as erro:
        if "conexao" in locals():
            conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")
        return False
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
           
def alt_pet():
    print("\n-----ALTERAR INFORMAÇÕES DE PET-----")

    pets = listar_disponiveis_pet()
    if not pets:
        print("Nenhum pet disponível para alteração.")
        return
    
    print("\n Lista de Pets Disponíveis:")

    for pet in pets:
        #Garante que se a raça for vazia, exiba "SRD" (Sem Raça Definida) na listagem
        raca_print = pet[3] if (len(pet) > 3 and pet[3]) else "SRD"
        print(f" - ID: {pet[0]} | Nome: {pet[1]} | Espécie: {pet[2]} | Raça: {raca_print}")
    print("-" * 40)

    try:
        id_input = input("Digite o ID do pet que deseja alterar: ").strip()
        if not id_input:
            print("ERRO: ID do pet é obrigatório.")
            return
        id_pet = int(id_input) # Se digitar letras, pula para o ValueError
    except ValueError:
        print("ERRO: O ID do pet deve ser um número válido.")
        return
    try:
        conexao = obter_conexao()
        if not conexao: 
            return False
        cursor = conexao.cursor()

    # Verifica se o Pet existe e se está ativo (Adicionei a busca por nome/especie/raca)
        cursor.execute("SELECT nome, especie, raca FROM Pet WHERE id = %s AND status = 1", (id_pet,))
        pet_atual = cursor.fetchone()

        if not pet_atual:
            print("ERRO: Pet não encontrado ou inativo.")
            return
        
        nome_atual = pet_atual[0]
        especie_atual = pet_atual[1]
        raca_atual = pet_atual[2]

        print(f"\nDados atuais -> Nome: {nome_atual} | Espécie: {especie_atual} | Raça: {raca_atual}")
        print("(Deixe em branco e pressione Enter para MANTER o dado atual)\n")

        #Validação novo nome
        novo_nome = input("Digite o novo nome do pet: ").strip().lower()
        if not novo_nome:
            novo_nome = nome_atual
        else:
            if any(caractere.isdigit() for caractere in novo_nome):
                print("ERRO: O nome do pet não pode conter números.")
                return

        #Validação nova especie 
        nova_especie = input("Digite a nova espécie: ").strip().lower()
        if not nova_especie:
            nova_especie = especie_atual

        #Validação nova raça
        nova_raca = input("Digite a nova raça: ").strip().lower()
        if not nova_raca:
            nova_raca = raca_atual

        #Atualiza os dados do pet no banco de dados
        cursor.execute(
            "UPDATE Pet SET nome = %s, especie = %s, raca = %s WHERE id = %s", 
            (novo_nome, nova_especie, nova_raca, id_pet)
        )

        conexao.commit()
        print(f"Pet com ID {id_pet} alterado com sucesso!")
    
    except mysql.connector.Error as erro:   
        if "conexao" in locals():
            conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")
        return False
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()       

def listar_disponiveis_pet():
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, especie, raca
            FROM pet
            WHERE status = 1
        """)

        pets = cursor.fetchall()
        return pets

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")
        pets = []
        return pets

    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()