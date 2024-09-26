import streamlit as st
from db_conn import fetch_data
import pandas as pd
import plotly.express as px

# Carregar dados
data = fetch_data()

# Configuração do layout com menu lateral
st.sidebar.title("Filtros")

# Filtros disponíveis
sexo_filter = st.sidebar.selectbox("Sexo", options=["Todos", "M", "F"])
relacao_filter = st.sidebar.multiselect("Relação", options=data['relacao'].unique(), default=data['relacao'].unique())
sociedade_filter = st.sidebar.multiselect("Sociedades", options=data['sociedade'].unique(), default=data['sociedade'].unique())

# Aplicar filtros de sexo, relação e sociedade primeiro
if sexo_filter != "Todos":
    data = data[data['sexo'] == sexo_filter]

if relacao_filter:
    data = data[data['relacao'].isin(relacao_filter)]

if sociedade_filter:
    data = data[data['sociedade'].isin(sociedade_filter)]

# Dicionário das áreas de interesse
areas_interesse = {
    "Comunicação": "area_interesse_comunicacao",
    "Evangelismo e Missões": "area_interesse_evangelismo_missoes",
    "Projeto Viver": "area_interesse_projeto_viver",
    "Departamento Infantil": "area_interesse_departamento_infantil",
    "Ação Social e Diaconia": "area_interesse_acao_social_diaconia",
    "Visitação": "area_interesse_visitacao",
    "Recepção": "area_interesse_recepcao",
    "Zeladoria": "area_interesse_zeladoria",
    "Eventos": "area_interesse_eventos",
    "Pregação": "area_interesse_pregacao",
    "Ensino": "area_interesse_ensino",
    "Secretaria": "area_interesse_secretaria",
    "Louvor": "area_interesse_louvor"
}

# Adiciona os filtros laterais para cada área
selected_areas = {}
for area, col in areas_interesse.items():
    selected_areas[area] = st.sidebar.slider(f"Prioridade {area}", 0, 5, (0, 5))

# Aplicar os filtros de áreas de interesse nos dados
for area, col in areas_interesse.items():
    min_val, max_val = selected_areas[area]
    data = data[(data[col] >= min_val) & (data[col] <= max_val)]

# Exibir dados filtrados
st.write("Dados Filtrados:")
st.dataframe(data)

# Seção de gráficos
st.sidebar.title("Gráficos")

# Opção para escolher o gráfico
graph_type = st.sidebar.selectbox(
    "Escolha o gráfico",
    ["Nenhum", "Prioridade Média por Área", "Distribuição de Áreas de Interesse"]
)

if graph_type == "Prioridade Média por Área":
    # Calcular a prioridade média por área
    priority_data = {area: data[col].mean() for area, col in areas_interesse.items()}
    
    # Exibir gráfico de barras usando Plotly
    st.write("Prioridade Média por Área de Interesse")
    fig = px.bar(x=list(priority_data.keys()), y=list(priority_data.values()), labels={'x': 'Área', 'y': 'Prioridade Média'}, title="Prioridade Média por Área")
    st.plotly_chart(fig)

elif graph_type == "Distribuição de Áreas de Interesse":
    # Contagem de prioridades para cada área e exibir gráfico de barras
    for area, col in areas_interesse.items():
        st.write(f"Distribuição das Prioridades na Área: {area}")
        counts = data[col].value_counts().sort_index()
        fig = px.bar(x=counts.index, y=counts.values, labels={'x': 'Prioridade', 'y': 'Contagem'}, title=f"Distribuição de Prioridades - {area}")
        st.plotly_chart(fig)
