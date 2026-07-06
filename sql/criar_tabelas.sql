CREATE DATABASE IF NOT EXISTS py_pets;
USE py_pets;

-- 1. TABELA CLIENTE
CREATE TABLE IF NOT EXISTS Cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(11) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    status TINYINT(1) NOT NULL DEFAULT 1 
);

-- 2. TABELA PET
CREATE TABLE IF NOT EXISTS Pet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(50) NOT NULL,
    id_cliente INT NOT NULL,
    status TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);

-- 3. TABELA PRODUTO 
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
);

-- 4. TABELA SERVICO
CREATE TABLE IF NOT EXISTS Servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(150),
    preco DECIMAL(10,2) NOT NULL,
    status TINYINT(1) NOT NULL DEFAULT 1
);

-- 5. TABELA AGENDAMENTO
CREATE TABLE IF NOT EXISTS Agendamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_hora DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Agendado',
    id_pet INT NOT NULL,
    FOREIGN KEY (id_pet) REFERENCES Pet(id)
);

-- 5.1 TABELA ASSOCIATIVA: AGENDAMENTO ↔ SERVICO
CREATE TABLE IF NOT EXISTS AgendamentoServico (
    id_agendamento INT NOT NULL,
    id_servico INT NOT NULL,
    preco_cobrado DECIMAL(10,2) NOT NULL, -- Preço do momento do agendamento (histórico)
    PRIMARY KEY (id_agendamento, id_servico),
    FOREIGN KEY (id_agendamento) REFERENCES Agendamento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES Servico(id)
);

-- 6. TABELA VENDA
CREATE TABLE IF NOT EXISTS Venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status TINYINT(1) NOT NULL DEFAULT 1
);

-- 7. TABELA ASSOCIATIVA: ITEM VENDA (Carrinho de compras)
-- ON DELETE CASCADE:  Se a venda principal (id) for excluída do banco, o MySQL apaga automaticamente todos os itens que pertenciam a ela.
CREATE TABLE IF NOT EXISTS ItemVenda (
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    qtd INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venda, id_produto),
    FOREIGN KEY (id_venda) REFERENCES Venda(id) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES Produto(id)
);