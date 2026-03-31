CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto VARCHAR(100),
    quantidade INT,
    preco DECIMAL(10,2),
    faturamento DECIMAL(10,2)
);