import mysql.connector

def load(df):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='@Welterson123',
        database='etl_db'
    )

    cursor = conn.cursor()

    # Cria a tabela se ela não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            produto VARCHAR(255),
            quantidade INT,
            preco DECIMAL(10, 2),
            faturamento DECIMAL(10, 2)
        )
    """)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO vendas (produto, quantidade, preco, faturamento)
            VALUES (%s, %s, %s, %s)
        """, (row['produto'], row['quantidade'], row['preco'], row['faturamento']))

    conn.commit()
    cursor.close()
    conn.close()