import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Carrega o dataset
df = pd.read_csv('vgsales.csv')

# Define as opções de filtro
region_options = ['NA', 'EU', 'JP', 'Other']
platform_options = ['Wii', 'NES', 'GB', 'DS', 'X360', 'PS3', 'PS2', 'SNES', 'GBA', 'PS4']
genre_options = ['Action', 'Sports', 'Shooter', 'Role-Playing', 'Platform']

# Define o título da página
st.title('Vendas de videogames')

# Define os filtros
region_filter = st.sidebar.selectbox('Região:', region_options)
platform_filter = st.sidebar.selectbox('Plataforma:', platform_options)
genre_filter = st.sidebar.selectbox('Gênero:', genre_options)

# Filtra os dados com base nas opções selecionadas
filtered_df = df[(df['Platform'] == platform_filter) & (df['Genre'] == genre_filter)]

# Agrupa os dados por ano e região e calcula as vendas totais
grouped_df = filtered_df.groupby(['Year', 'NA_Sales', 'EU_Sales', 'JP_Sales'])[['Global_Sales']].sum().reset_index()

# Cria um gráfico de linhas com as vendas globais por ano e região
fig = px.line(grouped_df, x='Year', y='Global_Sales', color_discrete_sequence=['blue'], title='Vendas globais de videogames')
fig.update_layout(xaxis_title='Ano', yaxis_title='Vendas globais (milhões)')
st.plotly_chart(fig)

# Cria um gráfico de barras com as vendas por região
region_df = filtered_df.groupby(['Year'])[region_filter + '_Sales'].sum().reset_index()
region_df.columns = ['Ano', 'Vendas']
fig2 = px.bar(region_df, x='Ano', y='Vendas', color_discrete_sequence=['red'], title=f'Vendas de {genre_filter} na {platform_filter} em {region_filter}')
fig2.update_layout(xaxis_title='Ano', yaxis_title=f'Vendas em {region_filter} (milhões)')
st.plotly_chart(fig2)
