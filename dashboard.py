import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from datetime import datetime

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── ESTILOS CUSTOMIZADOS ─────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Reset e base */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Fundo geral */
    .stApp {
        background: #0a0e1a;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0f1423;
        border-right: 1px solid rgba(99, 179, 237, 0.15);
    }
    [data-testid="stSidebar"] * {
        color: #a0aec0 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e2e8f0 !important;
    }

    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #141a2e 0%, #1a2240 100%);
        border: 1px solid rgba(99, 179, 237, 0.2);
        border-radius: 16px;
        padding: 28px 24px;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s ease;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #63b3ed, #805ad5);
        border-radius: 16px 16px 0 0;
    }
    .metric-card:hover {
        border-color: rgba(99, 179, 237, 0.4);
    }
    .metric-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #718096;
        margin-bottom: 12px;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 32px;
        font-weight: 600;
        color: #e2e8f0;
        line-height: 1;
        margin-bottom: 8px;
    }
    .metric-delta {
        font-size: 12px;
        color: #68d391;
        font-weight: 500;
    }
    .metric-icon {
        position: absolute;
        top: 24px; right: 24px;
        font-size: 28px;
        opacity: 0.4;
    }

    /* Header principal */
    .main-header {
        padding: 32px 0 24px;
        border-bottom: 1px solid rgba(99, 179, 237, 0.1);
        margin-bottom: 32px;
    }
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #e2e8f0;
        letter-spacing: -1px;
        margin: 0;
    }
    .main-subtitle {
        font-size: 14px;
        color: #4a5568;
        margin-top: 6px;
        font-weight: 400;
    }
    .badge {
        display: inline-block;
        background: rgba(99, 179, 237, 0.1);
        border: 1px solid rgba(99, 179, 237, 0.3);
        color: #63b3ed;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 12px;
    }

    /* Títulos de seção */
    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #a0aec0;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(99, 179, 237, 0.1);
    }

    /* Tabela */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(99, 179, 237, 0.15) !important;
    }
    [data-testid="stDataFrame"] > div {
        background: #0f1423;
        border-radius: 12px;
    }

    /* Divider */
    hr {
        border-color: rgba(99, 179, 237, 0.1) !important;
        margin: 32px 0 !important;
    }

    /* Selectbox / inputs */
    .stSelectbox > div > div {
        background: #141a2e;
        border-color: rgba(99, 179, 237, 0.2) !important;
        color: #e2e8f0 !important;
        border-radius: 10px;
    }

    /* Esconde elementos padrão do Streamlit */
    #MainMenu, footer, header {visibility: hidden;}

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e1a; }
    ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #4a5568; }
</style>
""", unsafe_allow_html=True)

# ─── CONEXÃO COM BANCO ────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def carregar_dados():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Welterson123',
            database='etl_db'
        )
        df = pd.read_sql("SELECT * FROM vendas", conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Controles")
    st.markdown("---")

    st.markdown("**🔄 Dados**")
    if st.button("Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("**📅 Filtros**")
    filtro_produto = st.text_input("🔍 Filtrar por produto", placeholder="Digite o nome...")

    st.markdown("---")
    st.markdown("**📊 Visualização**")
    tipo_grafico = st.selectbox(
        "Tipo de gráfico",
        ["Barras", "Pizza", "Linha", "Área"]
    )
    top_n = st.slider("Top N produtos", min_value=3, max_value=20, value=10)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px; color:#4a5568; text-align:center;'>"
        f"Última atualização<br>{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        "</div>",
        unsafe_allow_html=True
    )

# ─── CARREGAMENTO DOS DADOS ───────────────────────────────────────────────────
df, erro = carregar_dados()

if erro:
    st.error(f"❌ Erro ao conectar ao banco de dados: {erro}")
    st.stop()

if df is None or df.empty:
    st.warning("⚠️ Nenhum dado encontrado na tabela `vendas`.")
    st.stop()

# Aplicar filtro de produto
if filtro_produto:
    df_filtrado = df[df['produto'].str.contains(filtro_produto, case=False, na=False)]
else:
    df_filtrado = df

# ─── HEADER PRINCIPAL ─────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="badge">📊 Analytics</div>
    <h1 class="main-title">Dashboard de Vendas</h1>
    <p class="main-subtitle">Visão consolidada do desempenho comercial</p>
</div>
""", unsafe_allow_html=True)

# ─── MÉTRICAS ─────────────────────────────────────────────────────────────────
faturamento_total = df_filtrado['faturamento'].sum()
total_qtd = int(df_filtrado['quantidade'].sum())
total_registros = len(df_filtrado)
ticket_medio = faturamento_total / total_registros if total_registros > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-label">Faturamento Total</div>
        <div class="metric-value">R$ {faturamento_total:,.0f}</div>
        <div class="metric-delta">▲ acumulado</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-label">Unidades Vendidas</div>
        <div class="metric-value">{total_qtd:,}</div>
        <div class="metric-delta">▲ total de itens</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-label">Total de Registros</div>
        <div class="metric-value">{total_registros:,}</div>
        <div class="metric-delta">▲ transações</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-label">Ticket Médio</div>
        <div class="metric-value">R$ {ticket_medio:,.0f}</div>
        <div class="metric-delta">▲ por registro</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── GRÁFICOS ─────────────────────────────────────────────────────────────────
grafico_data = (
    df_filtrado.groupby('produto')['faturamento']
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
    .reset_index()
)
grafico_data.columns = ['Produto', 'Faturamento']

COLORS = ['#63b3ed', '#805ad5', '#68d391', '#f6ad55', '#fc8181',
          '#76e4f7', '#b794f4', '#9ae6b4', '#fbd38d', '#feb2b2']

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Space Grotesk', color='#a0aec0'),
    margin=dict(l=0, r=0, t=40, b=0),
    legend=dict(
        bgcolor='rgba(15,20,35,0.8)',
        bordercolor='rgba(99,179,237,0.2)',
        borderwidth=1,
    )
)

col_grafico, col_pizza = st.columns([3, 2])

with col_grafico:
    st.markdown('<div class="section-title">Faturamento por Produto</div>', unsafe_allow_html=True)

    if tipo_grafico == "Barras":
        fig = px.bar(
            grafico_data, x='Produto', y='Faturamento',
            color='Faturamento',
            color_continuous_scale=['#1a2240', '#63b3ed'],
        )
        fig.update_traces(marker_line_color='rgba(0,0,0,0)', marker_line_width=0)
        fig.update_coloraxes(showscale=False)

    elif tipo_grafico == "Linha":
        fig = px.line(
            grafico_data, x='Produto', y='Faturamento',
            markers=True,
            color_discrete_sequence=['#63b3ed'],
        )
        fig.update_traces(line_width=2.5, marker_size=8)

    elif tipo_grafico == "Área":
        fig = px.area(
            grafico_data, x='Produto', y='Faturamento',
            color_discrete_sequence=['#63b3ed'],
        )
        fig.update_traces(
            fillcolor='rgba(99,179,237,0.15)',
            line_color='#63b3ed',
            line_width=2,
        )

    else:  # Pizza (no col_grafico mostrar barras mesmo)
        fig = px.bar(
            grafico_data, x='Produto', y='Faturamento',
            color='Faturamento',
            color_continuous_scale=['#1a2240', '#63b3ed'],
        )
        fig.update_coloraxes(showscale=False)

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=360,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(99,179,237,0.07)', zeroline=False),
    )
    st.plotly_chart(fig, use_container_width=True)

with col_pizza:
    st.markdown('<div class="section-title">Distribuição</div>', unsafe_allow_html=True)

    fig_pie = go.Figure(data=[go.Pie(
        labels=grafico_data['Produto'],
        values=grafico_data['Faturamento'],
        hole=0.55,
        marker=dict(colors=COLORS, line=dict(color='#0a0e1a', width=2)),
        textinfo='percent',
        textfont=dict(size=11, color='#e2e8f0'),
    )])
    fig_pie.add_annotation(
        text=f"R$ {faturamento_total/1000:.0f}K",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color='#e2e8f0', family='JetBrains Mono'),
    )
    fig_pie.update_layout(**PLOTLY_LAYOUT, height=360, showlegend=True)
    st.plotly_chart(fig_pie, use_container_width=True)

# ─── TABELA DE DADOS ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">Registros de Vendas</div>', unsafe_allow_html=True)

col_busca, col_info = st.columns([3, 1])
with col_info:
    st.markdown(
        f"<div style='text-align:right; color:#4a5568; font-size:13px; padding-top:8px;'>"
        f"{len(df_filtrado):,} registros encontrados</div>",
        unsafe_allow_html=True
    )

# Formatar colunas numéricas se existirem
df_display = df_filtrado.copy()
if 'faturamento' in df_display.columns:
    df_display['faturamento'] = df_display['faturamento'].apply(lambda x: f"R$ {x:,.2f}")
if 'quantidade' in df_display.columns:
    df_display['quantidade'] = df_display['quantidade'].apply(lambda x: f"{int(x):,}")

st.dataframe(
    df_display,
    use_container_width=True,
    height=400,
    hide_index=True,
)

# ─── RODAPÉ ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#2d3748; font-size:12px; padding: 8px 0 24px;'>"
    "Dashboard de Vendas · Dados em tempo real · etl_db.vendas"
    "</div>",
    unsafe_allow_html=True
)