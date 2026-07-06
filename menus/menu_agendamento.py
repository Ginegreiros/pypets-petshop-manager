# menus/menu_agendamento.py
# Aqui fica só a interface (input/print do menu) e a navegação entre opções.
# As funções que falam direto com o banco moram em db/agendamentos_db.py.

import datetime

try:
    from db.agendamentos_db import listar_agendamento
except ImportError:
    print("Erro ao exportar informações")
    listar_agendamento = None

try:
    from db.agendamentos_db import buscar_agendamento
except ImportError:
    print("Erro ao exportar informações")
    buscar_agendamento = None

try:
    from db.agendamentos_db import cancelar_agendamento
except ImportError:
    print("Erro ao exportar informações")
    cancelar_agendamento = None

try:
    from db.agendamentos_db import confirmar_agendamento
except ImportError:
    print("Erro ao exportar informações")
    confirmar_agendamento = None

try:
    from db.agendamentos_db import criar_agendamento
except ImportError:
    print("Erro ao exportar informações")
    criar_agendamento = None

try:
    from db.servicos_db import listar_servicos
except ImportError:
    print("Erro ao exportar informações")
    listar_servicos = None

try:
    from db.pets_db import listar_disponiveis_pet
except ImportError:
    print("Erro ao exportar informações")
    listar_disponiveis_pet = None


#=========================================
#Bloco adicionado
try:
    from db.agendamentos_db import list_agend_pendentes
except ImportError:
    print("Erro ao exportar informações")
    list_agend_pendentes = None
#==========================================

# Só desenha a tela do menu. Não tem nenhuma lógica aqui, é chamada
# de novo a cada volta do loop em menu_agendamento()
def exibir_menu_agendamento():
    print("""
    ________________________________________
    |             MENU AGENDAMENTO         |
    |======================================|
    |  |1| - Novo Agendamento              |
    |  |2| - Listar Agendamentos           |
    |  |3| - Buscar Agendamento            |
    |  |4| - Confirmar/Concluir Agendamento|
    |  |5| - Cancelar Agendamento          |
    |  |0| - Sair Para Menu Principal      |
    |______________________________________|
    """)


def menu_agendamento():

    
    while True:
        exibir_menu_agendamento()

        # try/except protege contra letra digitada no lugar de número.
        try:
            opcao = int(input("Digite o comando: "))
        except ValueError:
            print("ERRO: O comando deve ser um número inteiro.")
            continue

        if opcao == 0:
            break

        elif opcao == 1:
            print("Atenção: só é possível agendar para pets já cadastrados. Veja a lista abaixo:")

            pets = listar_disponiveis_pet()

            if len(pets) == 0:
                print("ERRO: Nenhum pet cadastrado. Cadastre um pet antes de agendar.")
                continue

            for pet in pets:
                pet_id_lista, nome_pet, especie_pet, raca_pet = pet

                raca_print = raca_pet if raca_pet else "SRD"  # Se a raça for vazia, exibe "SRD"
                print(f"[{pet_id_lista}] {nome_pet} - {especie_pet} - {raca_print}")

            # Pede o ID do pet primeiro.
            try:
                pet_id = int(input("Digite o ID da Pet: "))
            except ValueError:
                print("ERRO: somente um número inteiro.")
                continue

            # Data é digitada manualmente (não automática), porque um
            # agendamento é sempre marcado pra um momento futuro escolhido
            # pelo cliente, não "agora"
            data_agendamento = input("Data DD/MM/YYYY HH:MM: ")

            # strptime converte o texto pra datetime e já valida o formato:
            # se não bater com DD/MM/AAAA HH:MM, lança ValueError
            try:
                data_convertida = datetime.datetime.strptime(data_agendamento, "%d/%m/%Y %H:%M")
            except ValueError:
                print("ERRO: Data inválida. Use o formato DD/MM/AAAA HH:MM.")
                continue

            # Regra do projeto: não aceitar agendamento no passado
            if data_convertida < datetime.datetime.now():
                print("ERRO: Não é possivel agendar uma data menor que atual.")
                continue

            # VERIFICAÇÃO DE HORÁRIO COMERCIAL: 09:00 - 18:00 

            # Bloqueia Domingos (No Python, os dias da semana vão de 0 a 6, sendo 0 = segunda-feira e 6 = domingo)
            if data_convertida.weekday() == 6:
                print("ERRO: Não é possível agendar aos domingos.")
                continue

            # Bloqueia horários fora do horário comercial (09:00 - 18:00)
            hora_agendamento = data_convertida.hour
            if hora_agendamento < 9 or hora_agendamento>=18:
                print("ERRO: Não é possível agendar fora do horário comercial (09:00 - 18:00).")
                continue

            #========================================

            # Busca os serviços cadastrados no banco (Banho, Tosa, etc)
            # pra mostrar como opção, em vez de ter isso fixo no código
            servicos = listar_servicos()

            # for servico in servicos:
            #     id_servico, nome_servico, descricao_servico, preco_servico = servico
            #     print(f"[{id_servico}] {nome_servico} - R$ {preco_servico:.2f}")

            # Usuário pode escolher mais de um serviço (ex: "1,2"), por isso
            # pegamos o texto puro primeiro e separamos por vírgula depois
            entrada_servicos = input("Digite ID dos serviços desejados: ")
            try:
                ids_escolhidos = [int(numero.strip()) for numero in entrada_servicos.split(",")]
            except ValueError:
                print("ERRO: Os IDs devem ser números inteiros separados por vírgula.")
                continue

            # Cruza cada ID escolhido com a lista de serviços do banco,
            # pra descobrir o preço de cada um e montar as tuplas
            # (id_servico, preco_cobrado) que criar_agendamento espera
            lista_servicos_escolhidos = []

            for id_escolhido in ids_escolhidos:
                for id_servico, nome_servico, descricao_servico, preco_servico in servicos:
                    if id_escolhido == id_servico:
                        lista_servicos_escolhidos.append((id_escolhido, preco_servico))

            # Se algum ID digitado não bateu com nenhum serviço da lista,
            # as duas listas ficam com tamanhos diferentes
            if len(lista_servicos_escolhidos) != len(ids_escolhidos):
                print("ERRO: Um ou mais IDs de serviço digitados não existem. Operação cancelada.")
                continue

            criar_agendamento(pet_id, data_convertida, lista_servicos_escolhidos)

        elif opcao == 2:
            listar_agendamento()

        elif opcao == 3:
            # Busca única que aceita nome do pet, data ou status no mesmo campo
            termo_busca = input("Digite o nome do pet, data ou status: ")
            buscar_agendamento(termo_busca)

        elif opcao == 4:

            list_agend_pendentes()
            try:
                busca_id = int(input("Digite o ID do agendamento que você quer confirmar: "))
                confirmar_agendamento(busca_id)
            except ValueError:
                print("ERRO: Somente um número inteiro.")

        elif opcao == 5:
            listar_agendamento()
            try:
                busca_id = int(input("Digite o ID do agendamento que você quer cancelar: "))
                cancelar_agendamento(busca_id)
            except ValueError:
                print("ERRO: Somente um número inteiro.")

        else:
            print(f"Você escolheu a opção {opcao}.")