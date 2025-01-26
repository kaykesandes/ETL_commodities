#import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Import das variáveis de ambiente
commodities = ['CL=f', 'GC=F', 'SI=F']

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# Verificar se todas as variáveis de ambiente estão definidas
if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, DB_SCHEMA]):
    raise ValueError("Uma ou mais variáveis de ambiente não estão definidas")

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Verificar a conexão com o banco de dados
try:
    with engine.connect() as connection:
        print("Conexão com o banco de dados estabelecida com sucesso.")
except OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit(1)

def buscar_dados_commodities(simbolo, periodo='5y', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

def salvar_dados_no_banco(df, schema='public'):
    df.to_sql('commodities', engine, schema=schema, if_exists='replace', index=True)

if __name__ == '__main__':
    dadosconcatenados = buscar_todos_dados_commodities(commodities)
    salvar_dados_no_banco(dadosconcatenados, schema=DB_SCHEMA)
    print("Extração e carga de dados concluída com sucesso.")