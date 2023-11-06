import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carrega o arquivo Excel
tecnico2018 = pd.read_excel("./db/tecnico2018.xlsx")

# Filtra os evadidos e concluintes
evadidos = tecnico2018[tecnico2018['Categoria da Situação'] == "Evadidos"]
concluintes = tecnico2018[tecnico2018['Categoria da Situação'] == "Concluintes"]

# Realiza o cálculo da taxa de evasão
evadidos1 = pd.crosstab(evadidos['Renda Familiar'], evadidos['Região'])
concluintes1 = pd.crosstab(concluintes['Renda Familiar'], concluintes['Região'])
teste = evadidos1 / (evadidos1 + concluintes1) * 100
dados = teste.loc[teste.index.isin([1, 2, 3, 4, 5, 7, 6])]
print(evadidos1)
print(teste)
print(dados)

# Define a página do Streamlit
st.title("Taxa de Evasão nos cursos técnicos por Região")

# Define o filtro por Região
regiao = st.selectbox("Região:", dados.columns)

# Cria o gráfico de barras com Matplotlib
plt.figure(figsize=(10, 6))
plt.bar(dados.index, dados[regiao], color='blue')
plt.title(f"Taxa de Evasão na Região {regiao}")
plt.xlabel("Renda Familiar Per Capita")
plt.ylabel("Taxa de Evasão (%)")
plt.ylim(0, 100)

st.pyplot(plt)

# Exibe os dados de origem
st.text("Dados: Plataforma Nilo Pecanha (2018)")
