# %%

import streamlit as st
import pandas as pd
import sqlalchemy
import os
import matplotlib.pyplot as plt
import seaborn as sn
from adjustText import adjust_text
from pathlib import Path

from utils import make_scatter, make_clusters

pasta_atual = Path(os.getcwd())

engine = sqlalchemy.create_engine('sqlite:///../../data/database.db')

with open(pasta_atual / 'etl_partidos.sql', 'r') as open_file:
    query = open_file.read()

df = pd.read_sql_query(query, engine)
df.head()

# %%

welcome = '''
# TSE Analytics - Eleições 2024

Uma iniciativa Téo Me Why em conjunto com a comunidade de análise e ciência de dados
'''

st.markdown(welcome)

uf_options = df['SG_UF'].unique().tolist()
uf_options.remove('BR')
uf_options = ['BR'] + uf_options

estado = st.sidebar.selectbox(label='Estado:', placeholder='Selecione o estado que deseja filtrar:', options=uf_options)
size = st.sidebar.checkbox('Tamanho das bolhas')
cluster = st.sidebar.checkbox('Definir cluster')
n_cluster = st.sidebar.number_input('Quantidade de clusters', value=6, format='%d', max_value=10, min_value=1)

data = df[df['SG_UF'] == estado]

if cluster:
    data = make_clusters(data, n_cluster)

fig = make_scatter(data, size=size, cluster=cluster)

st.pyplot(fig)