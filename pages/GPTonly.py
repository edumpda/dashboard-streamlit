import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io

# Dados fornecidos
data = """
Brasil,117976,42987,3478,39889,2719100488,34583,57638335
Norte,3830,1661,318,1074,119227482,1493,2179845
Amazonas,1076,360,13,406,86825350,322,1538628
Pará,1430,673,128,467,21503795,574,483651
Nordeste,14306,5314,324,4916,181117958,4050,4580917
Ceará,3501,1158,127,1010,34545322,915,826881
Pernambuco,3486,1546,5,1280,32958782,1289,1578243
Bahia,2985,734,47,1004,82996237,483,1546600
Sudeste,60423,20354,1614,20253,1855702209,16021,39757354
Minas Gerais,14085,5001,370,5195,228015736,3846,4491775
Espírito Santo,2502,953,140,738,40957723,764,1434527
Rio de Janeiro,6417,1617,77,2434,492762633,1302,6437956
São Paulo,37419,12783,1027,11887,1089487355,10108,27393095
Sul,32501,13370,1053,10731,481519629,11041,9368338
Paraná,10376,4155,245,3538,163507476,3331,3169921
Santa Catarina,10992,4576,391,3227,152806583,3671,2679866
Rio Grande do Sul,11133,4638,417,3966,165205570,4038,3518551
Centro-Oeste,6915,2288,169,2913,81533210,1979,1751881
Mato Grosso,1604,664,95,576,16556319,487,220947
Mato Grosso do Sul,-,-,-,-,-,-,-
Goiás,3941,1244,45,1937,44839246,1122,1011301
"""

# Transformar os dados em um DataFrame
df = pd.read_csv(io.StringIO(data), thousands=' ', delimiter=',', skipinitialspace=True, header=None)

# Definir os nomes das colunas com base no seu exemplo
df.columns = ['Brasil', 'Total', 'Inovacao_Processo', 'Projetos_Incompletos', 'Inovacao_Organizacional', 'Receita_Liquida_Vendas', 'Gastos_Numero_Empresas', 'Gastos_Valor']

# Reorganizar o DataFrame usando a função melt
df_melted = pd.melt(df, id_vars=['Brasil'], value_vars=['Inovacao_Processo', 'Projetos_Incompletos', 'Inovacao_Organizacional'],
                    var_name='Tipo_Inovacao', value_name='Numero_Empresas')

# Criar o aplicativo Streamlit
st.title('Dashboard de Inovação Empresarial no Brasil')

# 1. Gráfico de Barras para Número Total de Empresas por Região
st.subheader('Número Total de Empresas por Região')
fig1 = px.bar(df, x='Brasil', y='Total', color='Brasil', labels={'Total': 'Número de Empresas'})
st.plotly_chart(fig1)

# 2. Gráfico de Barras Empresas que Implementaram Inovação por Região
st.subheader('Empresas que Implementaram Inovação por Região')
fig2 = px.bar(df_melted, x='Brasil', y='Numero_Empresas', color='Tipo_Inovacao',
              labels={'Numero_Empresas': 'Número de Empresas', 'Tipo_Inovacao': 'Tipo de Inovação'},
              title='Empresas que Implementaram Inovação por Região')
st.plotly_chart(fig2)

# 3. Gráfico de Linhas para Receita Líquida de Vendas por Unidade Federativa (Atualizado)
st.subheader('Receita Líquida de Vendas por Unidade Federativa')
df_states_line = df[df['Brasil'] != 'Brasil']  # Excluir a linha de total do Brasil para o gráfico de linhas
fig3 = px.line(df_states_line, x='Brasil', y='Receita_Liquida_Vendas', markers=True)
fig3.update_layout(xaxis=dict(type='category'))  # Organizar os rótulos no eixo x
st.plotly_chart(fig3)

# 4. Gráfico de Pizza para Gastos em Inovação
st.subheader('Gastos em Inovação')
fig4 = px.pie(df, names='Brasil', values='Gastos_Valor',
              title='Gastos em Inovação por Região')
st.plotly_chart(fig4)

# 5. Gráfico de Barra para Dispendios realizados pelas empresas nas atividades inovativas por Região (Atualizado)
st.subheader('Dispendios realizados pelas empresas nas atividades inovativas por Região')
df_states_bar = df[df['Brasil'] != 'Brasil']  # Excluir a linha de total do Brasil para o gráfico de barras
fig5 = px.bar(df_states_bar, x='Brasil', y='Gastos_Valor')
fig5.update_layout(xaxis=dict(type='category'))  # Organizar os rótulos no eixo x
st.plotly_chart(fig5)

# 6. Gráfico de Dispersão para Total vs. Gastos em Inovação
st.subheader('Total vs. Gastos em Inovação')
fig6 = px.scatter(df, x='Total', y='Gastos_Valor',
                  title='Relação entre Total de Empresas e Gastos em Inovação por Região')
st.plotly_chart(fig6)
