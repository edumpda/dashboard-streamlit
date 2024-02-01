import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import seaborn as sns

# Função para carregar dados
def load_data(path=None):
    data = None
    if path is not None:
        data = pd.read_csv(path)
    else:
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
    return data

# Função para carregar o modelo
def load_model(path=None):
    model = None
    if path is not None:
        model = joblib.load(path)
    else:
        uploaded_file = st.file_uploader("Escolha um arquivo .joblib", type="joblib")
        if uploaded_file is not None:
            model = joblib.load(uploaded_file)
    return model

# Função para fazer previsões
def make_predictions(model, data):
    # Aqui, você adiciona uma coluna 'DRK_YN' ao DataFrame com as predições do modelo
    data['DRK_YN'] = model.predict(data)
    return data

# Função para criar gráficos
def create_plots(data):
    fig, axs = plt.subplots(nrows=3, figsize=(10,15))

    # Distribuição de sexo por consumo de álcool
    sns.countplot(x='sex', hue='DRK_YN', data=data, ax=axs[0])
    axs[0].set_title('Distribuição de sexo por consumo de álcool')

    # Distribuição de fumantes e não fumantes por sexo
    sns.countplot(x='sex', hue='SMK_stat_type_cd', data=data, ax=axs[1])
    axs[1].set_title('Distribuição de fumantes e não fumantes por sexo')

    # Distribuição de pessoas por faixa etária
    sns.histplot(data['age'], bins=10, ax=axs[2])
    axs[2].set_title('Distribuição de pessoas por faixa etária')

    st.pyplot(fig)