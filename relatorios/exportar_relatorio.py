
import datetime

try:

   from db.financeiro_db import buscar_dados_bi
except ImportError:
   buscar_dados_bi = None

try:
   from db.financeiro_db import buscar_ranking_produtos
except ImportError:
   buscar_ranking_produtos = None

try:
   from db.financeiro_db import buscar_ranking_servicos
except ImportError:
   buscar_ranking_servicos = None

def gerar_txt_fechamento():
    
   """
   Gera um relatório de fechamento de caixa num ficheiro .txt local.
   Utiliza dados simulados (stubs) para validar a operação física no sistema operativo
   até que as queries do banco de dados estejam prontas.
   """

   # Criação dinâmica do nome do ficheiro baseada na data e hora atual

   data_agora = datetime.datetime.now()
   nome_ficheiro = f"fechamento_{data_agora.strftime('%d-%m-%Y_%H-%M-%S')}.txt"

   # ==== BUSCA DOS DADOS REAIS ===== 

   dados_bi = buscar_dados_bi()

   if not dados_bi:

      print("\n[ERRO] Não foi possível buscar os dados do BI para gerar o relatório.")
      return
   
   total_vendas = dados_bi.get("total_vendas", 0)
   faturamento = dados_bi.get("faturamento", 0.0)

   ranking_produtos = buscar_ranking_produtos()
   ranking_servicos = buscar_ranking_servicos()

   # Pega o 1º colocado de cada ranking (se existir)
   produto_destaque = ranking_produtos[0][0] if ranking_produtos else "Nenhum produto vendido"
   servico_destaque = ranking_servicos[0][0] if ranking_servicos else "Nenhum serviço agendado"

   # ==== ESCRITA DO ARQUIVO ====== 

   try:
        
      #Abertura em modo 'w' (escrita) com instrução 'with' e codificação UTF-8

      with open(nome_ficheiro, 'w', encoding='utf-8') as ficheiro:
         
         ficheiro.write("==========================\n")
         ficheiro.write("\n PY PETS - FECHAMENTO DE CAIXA \n")
         ficheiro.write("==========================\n")
         ficheiro.write(f"Data/Hora da Emissão: {data_agora.strftime('%d/%m/%Y %H:%M:%S')}\n")

         ficheiro.write("\nRESUMO OPERACIONAL:\n")
         ficheiro.write(f" -> Total de Vendas: {total_vendas}\n")
         ficheiro.write(f" -> Receita Total: R$ {faturamento:.2f}\n\n")

         ficheiro.write("DESTAQUES DO DIA:\n")
         ficheiro.write(f" -> Produto mais vendido: { produto_destaque}\n")
         ficheiro.write(f" -> Serviço mais realizados: { servico_destaque}\n")

         ficheiro.write("\n==========================\n")
         ficheiro.write(f"Relatório de fechamento exportado localmente como '{nome_ficheiro}'.\n")

      print(f"\n[SUCESSO] Relatório de fechamento exportado localmente como '{nome_ficheiro}'.")

   except IOError as erro_sistema:

      print(f"\n[ERRO CRÍTICO] O sistema operativo bloqueou a gravação do ficheiro: {erro_sistema}")