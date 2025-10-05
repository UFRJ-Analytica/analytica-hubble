import streamlit as st
import pandas as pd
import numpy as np

# --- Configuração da Página ---
# Define o layout da página para ser um pouco mais largo
st.set_page_config(
    page_title="Radar de Inundações",
    layout="centered"
)

# --- Título e Subtítulo ---
# Usamos markdown para permitir a cor verde no título, como na imagem
st.markdown('<h1 style="color: lightgreen; text-align: center;">Radar de Inundações</h1>', unsafe_allow_html=True)
st.subheader("Selecione a área que deseja avaliar")

# --- Filtros de Seleção ---
# Cria duas colunas para colocar os seletores lado a lado
col1, col2 = st.columns(2)

with col1:
    # Dados de exemplo para as cidades
    cidades = ["Porto Alegre", "Recife", "Manaus", "São Paulo"]
    cidade_selecionada = st.selectbox(
        "Selecione a cidade",
        cidades,
        index=0  # Deixa Porto Alegre como padrão
    )

with col2:
    # Dados de exemplo para o período
    periodos = ["Últimos 30 dias", "Próximos 7 dias", "Análise Anual"]
    periodo_selecionado = st.selectbox(
        "Selecione o período",
        periodos
    )

st.write("---") # Linha divisória

# --- Seção do Mapa ---
st.subheader("Área de Risco de Inundação Prevista")

# Dados de exemplo para o mapa (latitude e longitude de Porto Alegre)
map_data = pd.DataFrame({
    'lat': [-30.0346],
    'lon': [-51.2177]
})

# Exibe um mapa simples focado na coordenada. Em um projeto real,
# aqui você adicionaria camadas de risco (polígonos).
st.map(map_data, zoom=11)


# --- Seção de Nível de Risco ---
st.subheader("Nível de Risco", help="Este valor representa a probabilidade e o impacto de uma inundação, numa escala de 1 a 10.")

# Cria duas colunas para as métricas de risco
col_risco, col_populacao = st.columns(2)

with col_risco:
    # Métrica para o nível de risco
    st.metric(label="Risco de Inundação", value="5 / 10")

with col_populacao:
    # Métrica para a população afetada
    st.metric(label="População Afetada Estimada", value="10 mil")


# --- Botão de Ajuda ---
if st.button("Entenda o Nível de Risco"):
    st.info("""
    **Como o Risco é Calculado:**
    - **1-3 (Baixo):** Condições históricas normais, baixa probabilidade de inundação.
    - **4-6 (Moderado):** Alerta para chuvas acima da média histórica. Requer monitoramento.
    - **7-10 (Alto):** Grande probabilidade de inundação com base em dados de chuva, população e histórico de desastres.
    """)