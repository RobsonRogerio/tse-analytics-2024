# %%

import streamlit as st
import pandas as pd
import sqlalchemy
import os
from pathlib import Path

pasta_atual = Path(os.getcwd())

engine = sqlalchemy.create_engine('sqlite:///../../data/database.db')

with open(pasta_atual / 'etl_partidos.sql', 'r') as open_file:
    query = open_file.read()

df = pd.read_sql_query(query, engine)
df.head()

# %%

welcome = '''
# TSE Analytics - Eleições 2024

Uma iniciativa Teo Me Why em conjunto com a comunidade de análise e ciência de dados
'''

st.markdown(welcome)

uf_options = df['SG_UF'].unique().tolist()
uf_options.remove('BR')
uf_options = ['BR'] + uf_options

estado = st.selectbox(label='Estado', placeholder='Selecione o estado que deseja filtrar:', options=uf_options)

df_uf = df[df['SG_UF'] == estado]

st.dataframe(df_uf)

# %%
