import streamlit as st
import pandas as pd
import mysql.connector

# conexão com banco
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='@Welterson123',
    database='etl_db'
)

# carregar dados
query = "SELECT * FROM vendas"
df = pd.read_sql(query, conn)

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title("📊 Dashboard de Vendas")

# métricas
col1, col2, col3 = st.columns(3)

col1.metric("💰 Faturamento Total", f"R$ {df['faturamento'].sum():,.2f}")
col2.metric("📦 Total de Produtos", int(df['quantidade'].sum()))
col3.metric("🛒 Total de Registros", len(df))

st.divider()

# tabela
st.subheader("📋 Dados de Vendas")
st.dataframe(df)

st.divider()

# gráfico
st.subheader("📊 Faturamento por Produto")
grafico = df.groupby('produto')['faturamento'].sum()
st.bar_chart(grafico)