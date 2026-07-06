# 🐾 PyPets — Sistema de Gestão para Petshop

🇧🇷 [Português](#-português) | 🇺🇸 [English](#-english)

---

## 🇧🇷 Português

Sistema de linha de comando (CLI) para gestão de clientes, pets, agendamentos,
vendas, estoque e financeiro de um petshop, feito em Python com MySQL.

### 🚀 Funcionalidades
- Cadastro de clientes e pets (com ativação/desativação)
- Agendamento de serviços (banho, tosa, etc.)
- Controle de estoque e vendas de produtos
- Relatórios financeiros (fechamento de caixa, ranking de produtos/serviços)

### 🛠️ Tecnologias
- Python 3.14
- MySQL
- mysql-connector-python
- python-dotenv

### 📦 Como rodar o projeto
1. Clone o repositório:
```bash
git clone https://github.com/Ginegreiros/pypets-petshop-manager.git
cd pypets-petshop-manager
```
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\Activate
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Copie o arquivo de exemplo de variáveis de ambiente e preencha com seus dados:
```bash
copy .env.example .env
```
5. Execute o sistema:
```bash
python main.py
```

### 🗂️ Estrutura do projeto
```
petshop/
├── main.py
├── conexao.py
├── db/          # Regras de acesso a dados (SQL)
├── menus/       # Camada de interação com o usuário (CLI)
├── relatorios/  # Geração de relatórios
└── sql/         # Criação/inicialização do banco
```

### 📸 Demonstração
*(em breve — print ou GIF do sistema rodando)*

### 📄 Licença
Este projeto está sob a licença MIT.

---

## 🇺🇸 English

Command-line (CLI) system for managing customers, pets, appointments, sales,
inventory, and finances for a pet shop, built with Python and MySQL.

### 🚀 Features
- Customer and pet registration (with activation/deactivation)
- Service scheduling (bathing, grooming, etc.)
- Product inventory and sales control
- Financial reports (cash closing, product/service rankings)

### 🛠️ Tech Stack
- Python 3.14
- MySQL
- mysql-connector-python
- python-dotenv

### 📦 How to run the project
1. Clone the repository:
```bash
git clone https://github.com/Ginegreiros/pypets-petshop-manager.git
cd pypets-petshop-manager
```
2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\Activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Copy the example environment file and fill in your own values:
```bash
copy .env.example .env
```
5. Run the system:
```bash
python main.py
```

### 🗂️ Project structure
```
petshop/
├── main.py
├── conexao.py
├── db/          # Data access layer (SQL)
├── menus/       # CLI interaction layer
├── relatorios/  # Report generation
└── sql/         # Database creation/initialization
```

### 📸 Demo
*(coming soon — screenshot or GIF of the system running)*

### 📄 License
This project is licensed under the MIT License.
