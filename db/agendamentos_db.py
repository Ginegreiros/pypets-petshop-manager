# db/agendamentos_db.py
# Aqui ficam só as funções que falam direto com o banco (queries SQL).
# A parte de interface (input/print de menu) mora em menus/menu_agendamento.py.

import mysql.connector

try:
    from conexao import obter_conexao
except ImportError:
    print("Erro ao exportar informações")
    obter_conexao = None


def listar_agendamento():
    print("\n========== LISTA DE AGENDAMENTOS ==========")
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # JOIN triplo: agendamento -> pet -> cliente, pra exibir nome em vez de só ID
        cursor.execute("""
            SELECT 
                agendamento.id,
                pet.nome,
                pet.especie,
                cliente.nome,
                agendamento.data_hora,
                agendamento.status,
                GROUP_CONCAT(servico.nome SEPARATOR ', ')
            FROM agendamento
            INNER JOIN pet ON agendamento.id_pet = pet.id
            INNER JOIN cliente ON pet.id_cliente = cliente.id
            INNER JOIN agendamentoservico ON agendamento.id = agendamentoservico.id_agendamento
            INNER JOIN servico ON agendamentoservico.id_servico = servico.id
            GROUP BY agendamento.id
        """)

        agendamentos = cursor.fetchall()

        # Se não veio nenhuma linha, avisa e encerra a função aqui mesmo
        if not agendamentos:
            print("Nenhum agendamento cadastrado ainda.")
            return

        # Cada "agendamento" aqui é uma tupla: (id, nome_pet, nome_cliente, data_hora, status)
        for agendamento in agendamentos:
            id_agendamento, nome_pet, especie_pet, nome_cliente, data_hora, status, servicos_nomes = agendamento

            #Aplica a formatação de data/hora para exibir no formato brasileiro
            data_formatada = data_hora.strftime("%d/%m/%Y %H:%M")

            print(f"""
            _________________________________________
                ID Agendamento: {id_agendamento}
                Pet: {nome_pet} ({especie_pet})
                Cliente: {nome_cliente}
                Data/Hora: {data_formatada}
                Status: {status}
                Serviços: {servicos_nomes}        
             _______________________________________
                  """)

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")

    finally:
        # Sempre libera a conexão, com erro ou sem erro
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def criar_agendamento(id_pet, data_hora, lista_servicos):
    """
    Cria um novo agendamento e vincula um ou mais serviços a ele.
    """
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # 1) Insere o agendamento principal primeiro
        cursor.execute(
            "INSERT INTO agendamento (data_hora, status, id_pet) VALUES (%s, %s, %s)",
            (data_hora, "Agendado", id_pet),
        )

        # cursor.lastrowid pega o ID que o AUTO_INCREMENT acabou de gerar
        # pra esse agendamento, sem precisar de um SELECT extra
        id_novo_agendamento = cursor.lastrowid

        # 2) Insere uma linha em agendamentoservico pra cada serviço escolhido
        for id_servico, preco_cobrado in lista_servicos:
            cursor.execute(
                "INSERT INTO agendamentoservico (id_agendamento, id_servico, preco_cobrado) VALUES (%s, %s, %s)",
                (id_novo_agendamento, id_servico, preco_cobrado),
            )

        # Só confirma no banco (commit) depois que todos os inserts deram certo
        conexao.commit()
        print(f"Agendamento criado com sucesso! (ID: {id_novo_agendamento})")

    except mysql.connector.Error as erro:
        # Se falhar no meio do caminho, desfaz tudo (inclusive o agendamento)
        conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")

    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def cancelar_agendamento(id_agendamento):
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Busca o status atual antes de qualquer alteração, pra validar se esse agendamento pode ser cancelado ou não
        cursor.execute(
            "SELECT status FROM agendamento WHERE id = %s", (id_agendamento,)
        )
        resultado = cursor.fetchone()

        # fetchone() retorna None quando nao encontra nenhuma linha com esse id
        if resultado is None:
            print("ERRO: Agendamento não encontrado.")
            return

        status_atual = resultado[0]

        # Nao faz sentido cancelar um agendamento que ja aconteceu
        if status_atual == "Concluido":
            print("ERRO: Não é possível cancelar um agendamento já concluído.")
            return

        # Evita reprocessar um cancelamento que ja foi feito antes
        if status_atual == "Cancelado":
            print("ERRO: Este agendamento já está cancelado.")
            return

        # Soft delete: nunca usamos DELETE aqui, só trocamos o status.
        cursor.execute(
            "UPDATE agendamento SET status = %s WHERE id = %s",
            ("Cancelado", id_agendamento),
        )
        conexao.commit()
        print("Agendamento cancelado com sucesso.")

    except mysql.connector.Error as erro:
        # Desfaz qualquer alteracao parcial se algo der errado
        conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")

    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def confirmar_agendamento(id_agendamento):
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Busca o status atual antes de qualquer alteração, pra validar se esse agendamento pode ser concluida ou não
        cursor.execute("SELECT status FROM agendamento WHERE id = %s", (id_agendamento,))
        resultado = cursor.fetchone()

        # fetchone() retorna None quando nao encontra nenhuma linha com esse id 
        if resultado is None:
            print("ERRO: Agendamento não encontrado.")
            return

        status_atual = resultado[0]

        # Evita reprocessar que ja foi feito antes
        if status_atual == "Concluido":
            print("ERRO: Este agendamento já está concluído.")
            return

        # Nao faz sentido concluir um agendamento que ja foi cancelado.
        if status_atual == "Cancelado":
            print("ERRO: Não é possivel confirmar um agendamento já cancelado.")
            return

        # Soft update: registra que o atendimento aconteceu de fato, sem apagar nada
        cursor.execute(
            "UPDATE agendamento SET status = %s WHERE id = %s",
            ("Concluido", id_agendamento),
        )
        conexao.commit()
        print("Agendamento concluido com sucesso.")

    except mysql.connector.Error as erro:
        # Desfaz qualquer alteracao parcial se algo der errado
        conexao.rollback()
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")

    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def buscar_agendamento(termo_busca):
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Filtro unico que busca o termo digitado em 3 campos ao mesmo tempo
        # (nome do pet, status ou data), usando OR pra bastar bater em um deles.
        # O DATE_FORMAT é usado pra formatar a data/hora do banco (que vem como datetime) em string no formato brasileiro, pra poder comparar com o termo digitado.
        cursor.execute("""
            SELECT agendamento.id, pet.nome, cliente.nome, agendamento.data_hora, agendamento.status
            FROM agendamento
            INNER JOIN pet ON agendamento.id_pet = pet.id
            INNER JOIN cliente ON pet.id_cliente = cliente.id
            WHERE pet.nome LIKE %s
                OR agendamento.status LIKE %s
                OR DATE_FORMAT(agendamento.data_hora, '%d/%m/%Y') LIKE %s
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultados = cursor.fetchall()

        # Lista vazia significa que nenhum dos 3 campos bateu com o termo buscado
        if len(resultados) == 0:
            print("Nenhum agendamento encontrado.")
            return

        for linha in resultados:
            id_agendamento, nome_pet, nome_cliente, data_hora, status = linha

            data_formatada = data_hora.strftime("%d/%m/%Y %H:%M")

            print(f"""
_____________________________________
ID Agendamento: {id_agendamento} 
Pet:            {nome_pet}                  
Cliente:        {nome_cliente}          
Data/Hora:      {data_formatada}           
Status:         {status}                 
_____________________________________                 
""")

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE BANCO DE DADOS: {erro}")

    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


#==================================================================
#Função adicionada - Heverton Oliveira
#Semelhante a função "listar_agendamento"
#Porém com aplicação de " WHERE agendamento.status = 'Agendado' "
#Pequena mudança, grande diferença!

def list_agend_pendentes():
    """Lista apenas agendamentos com status 'Agendado', para a tela de conclusão."""
    print("\n========== AGENDAMENTOS PENDENTES ==========")
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT 
                agendamento.id,
                pet.nome,
                pet.especie,
                cliente.nome,
                agendamento.data_hora,
                agendamento.status,
                GROUP_CONCAT(servico.nome SEPARATOR ', ')
            FROM agendamento
            INNER JOIN pet ON agendamento.id_pet = pet.id
            INNER JOIN cliente ON pet.id_cliente = cliente.id
            INNER JOIN agendamentoservico ON agendamento.id = agendamentoservico.id_agendamento
            INNER JOIN servico ON agendamentoservico.id_servico = servico.id
            WHERE agendamento.status = 'Agendado'
            GROUP BY agendamento.id
        """)

        agendamentos = cursor.fetchall()

        if not agendamentos:
            print("Nenhum agendamento pendente no momento.")
            return

        for agendamento in agendamentos:
            id_agendamento, nome_pet, especie_pet, nome_cliente, data_hora, status, servicos_nomes = agendamento
            data_formatada = data_hora.strftime("%d/%m/%Y %H:%M")
            print(f"""
_________________________________________
ID Agendamento: {id_agendamento}
Pet:            {nome_pet} ({especie_pet})
Cliente:        {nome_cliente}
Data/Hora:      {data_formatada}
Status:         {status}
Serviços:       {servicos_nomes}        
_________________________________________
                  """)

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")

    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def list_agend_concluidos():
    """Lista apenas agendamentos com status 'Concluido', para a emissão de nota fiscal de serviço."""
    print("\n========== AGENDAMENTOS CONCLUÍDOS ==========")
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT 
                agendamento.id,
                pet.nome,
                pet.especie,
                cliente.nome,
                agendamento.data_hora,
                agendamento.status,
                GROUP_CONCAT(servico.nome SEPARATOR ', ')
            FROM agendamento
            INNER JOIN pet ON agendamento.id_pet = pet.id
            INNER JOIN cliente ON pet.id_cliente = cliente.id
            INNER JOIN agendamentoservico ON agendamento.id = agendamentoservico.id_agendamento
            INNER JOIN servico ON agendamentoservico.id_servico = servico.id
            WHERE agendamento.status = 'Concluido'
            GROUP BY agendamento.id
        """)

        agendamentos = cursor.fetchall()

        if not agendamentos:
            print("Nenhum agendamento concluído no momento.")
            return

        for agendamento in agendamentos:
            id_agendamento, nome_pet, especie_pet, nome_cliente, data_hora, status, servicos_nomes = agendamento
            data_formatada = data_hora.strftime("%d/%m/%Y %H:%M")
            print(f"""
_________________________________________
ID Agendamento: {id_agendamento}
Pet:            {nome_pet} ({especie_pet})
Cliente:        {nome_cliente}
Data/Hora:      {data_formatada}
Status:         {status}
Serviços:       {servicos_nomes}        
_________________________________________
                  """)

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")

    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()