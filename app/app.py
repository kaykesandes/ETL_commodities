import os
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# Criar a URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

def get_data():
    query = f"""
    SELECT
        data,
        simbolo,
        valor_fechamento,
        acao,
        quantidade,
        valor,
        ganho
    FROM
        public.dm_commodities;
    """
    df = pd.read_sql(query, engine)
    return df

# Configurar a página do Streamlit
st.set_page_config(page_title='Dashboard do diretor', layout='wide')

# Título do Dashboard
st.title('Dashboard de Commodities')

# Descrição
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stTitle {
        color: #4CAF50;
    }
    .stMarkdown {
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.write("""
Este dashboard mostra os dados de commodities e suas transações.
""")

# Obter os dados
df = get_data()

# Mostrar os dados em uma tabela
st.dataframe(df)

# Gráfico de linha para valor de fechamento ao longo do tempo
fig = px.line(df, x='data', y='valor_fechamento', color='simbolo', title='Valor de Fechamento ao Longo do Tempo')
st.plotly_chart(fig)

# Gráfico de barras para quantidade de ações por símbolo
fig = px.bar(df, x='simbolo', y='quantidade', color='simbolo', title='Quantidade de Ações por Símbolo')
st.plotly_chart(fig)

# Gráfico de dispersão para valor vs ganho
fig = px.scatter(df, x='valor', y='ganho', color='simbolo', title='Valor vs Ganho')
st.plotly_chart(fig)