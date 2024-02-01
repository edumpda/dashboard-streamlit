import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import seaborn as sns
import os
import smokers


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

def main():
    st.title('Streamlit + Chat GPT')

    if 'option' not in st.session_state:
        st.session_state['option'] = None

    if st.button('Subir meu próprio modelo e base'):
        st.session_state['option'] = 'upload'
    elif st.button('Testar modelos e bases existentes'):
        st.session_state['option'] = 'test'

    if st.session_state['option'] == 'upload':
        data = smokers.load_data()

        if data is not None:
            st.write(data)

            model = smokers.train_model(data)

            if model is not None:
                data_with_predictions = smokers.make_predictions(model, data)
                fig = smokers.create_plots(data_with_predictions)
                st.pyplot(fig)
    elif st.session_state['option'] == 'test':
        dataset_name_placeholder = st.empty()
        model_name_placeholder = st.empty()
        confirm_button_placeholder = st.empty()

        dataset_name = dataset_name_placeholder.selectbox(
            'Escolha um conjunto de dados',
            [''] + os.listdir('./db/datasets'))

        if dataset_name:
            model_name = model_name_placeholder.selectbox(
                'Escolha um modelo',
                [''] + os.listdir(f'./db/modelsPT/{dataset_name}'))

            if model_name and confirm_button_placeholder.button('Confirmar'):
                data = smokers.load_data(f'./db/datasets/{dataset_name}')
                model = smokers.load_model(f'./db/modelsPT/{dataset_name}/{model_name}')

                data_with_predictions = smokers.make_predictions(model, data)
                fig = smokers.create_plots(data_with_predictions)
                st.pyplot(fig)

if __name__ == "__main__":
    main()
