# %%

import streamlit as st
import pandas as pd
import sqlalchemy
import os
import gdown

from utils import make_scatter, make_clusters

app_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(app_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, 'data')

st.cache_data(ttl=60*60*24)
def create_df():
    filename = os.path.join(data_path, 'data_partidos.parquet')
    return pd.read_parquet(filename)


    
# %%

df = create_df()

welcome = '''
# TSE Analytics - Eleições 2024

Uma iniciativa Téo Me Why em conjunto com a comunidade de análise e ciência de dados
'''

st.markdown(welcome)

uf_options = df['SG_UF'].unique().tolist()
uf_options.sort()
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