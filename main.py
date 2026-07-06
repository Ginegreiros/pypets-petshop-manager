
import mysql.connector

# py_pets/main.py

#importa a sua função do módulo de menus

from menus.menu_principal import exibir_menu_principal
from sql.db import iniciar_db

iniciar_db()

#Ponto de entrada, o interpretador vai ler este arquivo, ver que ele é o código principal, e iniciar o menu.
# ==========================================
# PONTO DE ENTRADA DO SISTEMA (ENTRY POINT)
# Garante que o menu principal só seja executado se este arquivo 
# for rodado diretamente no terminal (ex: python main.py). 
# Impede que o sistema inicie acidentalmente caso este arquivo 
# seja apenas importado por outro módulo do projeto.
# ==========================================

if __name__ == "__main__":
    exibir_menu_principal()