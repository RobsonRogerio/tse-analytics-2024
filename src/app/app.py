# %%

import streamlit as st
import pandas as pd
import os

from utils import make_scatter, make_clusters

app_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(app_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, 'data')

st.cache_data(ttl=60*60*24)
def create_df():
    filename = os.path.join(data_path, 'data_partidos.parquet')
    return pd.read_parquet(filename)

features_map = {
    'PERCENTUAL FEMININO': 'TX_GEN_FEMININO',
    'PERCENTUAL PESSOAS PRETAS': 'TX_COR_RACA_PRETA',
    'PERCENTUAL PESSOAS PRETAS E PARDAS': 'TX_COR_RACA_PRETA_PARDA',
    'PERCENTUAL PESSOAS NÃO BRANCAS': 'TX_COR_RACA_NAO_BRANCA',
    'MÉDIA VALOR BENS': 'AVG_BENS',
    'MÉDIA VALOR BENS SEM ZEROS': 'AVG_BENS_NOT_ZERO',
    'PERCENTUAL CASADOS': 'TX_EST_CIVIL_CASADO',
    'PERCENTUAL SOLTEIROS': 'TX_EST_CIVIL_SOLTEIRO',
    'PERCENTUAL SEPARADOS/DIVORCIADOS': 'TX_EST_CIVIL_SEP_DIVORC',
    'MÉDIA IDADE': 'AVG_IDADE',
}

features_options = list(features_map.keys())
features_options.sort()
    
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

cargos_options = df['DS_CARGO'].unique().tolist()
cargos_options.sort()
cargos_options.remove('GERAL')
cargos_options = ['GERAL'] + cargos_options

# Definicão do estado e cargo
col1, col2 = st.columns(2)
with col1:
    estado = st.selectbox(label='Estado:', placeholder='Selecione o estado', options=uf_options)

with col2:
    cargo = st.selectbox(label='Cargo', placeholder='Selecione o cargo', options=cargos_options)

# Definição dos eixos x, y
col1, col2 = st.columns(2)
with col1:
    x_option = st.selectbox(label='Eixo X', options=features_options, index=4)
    x = features_map[x_option]
    new_features_options = features_options.copy()
    new_features_options.remove(x_option)

with col2:
    y_option = st.selectbox(label='Eixo Y', options=features_options, index=6)
    y = features_map[y_option]

size = st.checkbox('Tamanho das bolhas')

# Definição de clusters
col1, col2 = st.columns(2)
with col1:
    cluster = st.checkbox('Definir cluster')
    if cluster:
        n_cluster = st.number_input('Quantidade de clusters', value=6, format='%d', max_value=10, min_value=1)

with col2:
    if cluster:
        features_options_selected = st.multiselect(label='Opções para clusterização',
                                                   options=features_options,
                                                   default= ['PERCENTUAL FEMININO','PERCENTUAL PESSOAS PRETAS'])
        features_selected = [features_map[i] for i in features_options_selected]


data = df[(df['SG_UF'] == estado) & (df['DS_CARGO'] == cargo)].copy()

total_candidatos = int(data['TOTAL_CANDIDATURAS'].sum())
st.markdown(f'Total de candidaturas: {total_candidatos}')

if cluster:
    data = make_clusters(data=data, features=[x, y], n=n_cluster)

fig = make_scatter(
                data,
                x=x,
                y=y,
                x_label=x_option,
                y_label=y_option,
                cluster=cluster,
                size=size
                )

st.pyplot(fig)
# %%
