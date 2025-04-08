# %%

import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sn
from adjustText import adjust_text


# %%
with open('partidos.sql', 'r') as open_file:
    query = open_file.read()

engine = sqlalchemy.create_engine('sqlite:///../data/database.db')

df = pd.read_sql_query(query, engine)

df.head()

# %%

TX_GEN_FEMININO = df['TOTAL_GEN_FEMININO'].sum() / df['TOTAL_CANDIDATURAS'].sum()
TX_COR_RACA_PRETA = df['TOTAL_COR_RACA_PRETA'].sum() / df['TOTAL_CANDIDATURAS'].sum()
TX_COR_RACA_NAO_BRANCA = df['TOTAL_COR_RACA_NAO_BRANCA'].sum() / df['TOTAL_CANDIDATURAS'].sum()
TX_COR_RACA_PRETA_PARDA = df['TOTAL_COR_RACA_PRETA_PARDA'].sum() / df['TOTAL_CANDIDATURAS'].sum()


# %%

plt.figure(dpi=360, figsize=(6,5.5))

sn.scatterplot(data=df, 
               x='TX_GEN_FEM_BR', 
               y='TX_COR_RACA_PRETA_BR',
               )

texts = []
for i in df['SG_PARTIDO']:
    data = df[df['SG_PARTIDO'] == i]
    x = data['TX_GEN_FEM_BR'].values[0]
    y = data['TX_COR_RACA_PRETA_BR'].values[0]
    texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts, only_move={'points': 'y', 'texts': 'y'}, arrowprops=dict(arrowstyle="-"))

plt.grid(True)
plt.title('Cor vs Gênero - Eleições 2024')
plt.xlabel('Taxa de Mulheres')
plt.ylabel('Taxa de Pessoas Pretas')

plt.hlines(y=TX_COR_RACA_PRETA, xmin=0.30, xmax=0.55, colors='black', linestyles='--', label=f'% Pessoas Pretas: {100*TX_COR_RACA_PRETA:.0f}%')
plt.vlines(x=TX_GEN_FEMININO, ymin=0.05, ymax=0.35, colors='tomato', linestyles='--', label=f'% Mulheres: {100*TX_GEN_FEMININO:.0f}%')

plt.legend()

plt.savefig('../img/partidos_cor_raca_genero.png')


# %%
plt.figure(dpi=360, figsize=(6,5.5))

sn.scatterplot(data=df, 
               x='TX_GEN_FEM_BR', 
               y='TX_COR_RACA_PRETA_BR',
               size='TOTAL_CANDIDATURAS',
               sizes=(5,200)
               )

texts = []
for i in df['SG_PARTIDO']:
    data = df[df['SG_PARTIDO'] == i]
    x = data['TX_GEN_FEM_BR'].values[0]
    y = data['TX_COR_RACA_PRETA_BR'].values[0]
    texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts, only_move={'points': 'y', 'texts': 'y'}, arrowprops=dict(arrowstyle="-"))

plt.grid(True)
plt.title('Cor vs Gênero - Eleições 2024')
plt.xlabel('Taxa de Mulheres')
plt.ylabel('Taxa de Pessoas Pretas')

plt.hlines(y=TX_COR_RACA_PRETA, xmin=0.30, xmax=0.55, colors='black', linestyles='--', label=f'% Pessoas Pretas: {100*TX_COR_RACA_PRETA:.0f}%')
plt.vlines(x=TX_GEN_FEMININO, ymin=0.05, ymax=0.35, colors='tomato', linestyles='--', label=f'% Mulheres: {100*TX_GEN_FEMININO:.0f}%')

plt.legend()

handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[5:]
labels = labels[5:]  

plt.legend(handles=handles, labels=labels)

plt.savefig('../img/partidos_cor_raca_genero_bolha_size.png')

# %%

from sklearn import cluster

X = df[['TX_GEN_FEM_BR', 'TX_COR_RACA_PRETA_BR']]

model = cluster.KMeans(n_clusters=5)
model.fit(X)

df['clusterBR'] = model.labels_
df.groupby(['clusterBR'])['TX_GEN_FEM_BR'].count()

# %%
plt.figure(dpi=360, figsize=(6,5.5))

sn.scatterplot(data=df, 
               x='TX_GEN_FEM_BR', 
               y='TX_COR_RACA_PRETA_BR',
               size='TOTAL_CANDIDATURAS',
               sizes=(5,300),
               hue='clusterBR',
               palette='viridis',
               alpha=0.6,
               )

texts = []
for i in df['SG_PARTIDO']:
    data = df[df['SG_PARTIDO'] == i]
    x = data['TX_GEN_FEM_BR'].values[0]
    y = data['TX_COR_RACA_PRETA_BR'].values[0]
    texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts, only_move={'points': 'y', 'texts': 'y'}, arrowprops=dict(arrowstyle="-"))

plt.grid(True)
plt.suptitle('Partidos: Cor vs Gênero - Eleições 2024')
plt.title('Tamanho bolha = Qtde. Candidatos do Partido', fontdict={'size': 9})
plt.xlabel('Taxa de Mulheres')
plt.ylabel('Taxa de Pessoas Pretas')

plt.hlines(y=TX_COR_RACA_PRETA, xmin=0.30, xmax=0.55, colors='black', alpha=0.6, linestyles='--', label=f'% Pessoas Pretas: {100*TX_COR_RACA_PRETA:.0f}%')
plt.vlines(x=TX_GEN_FEMININO, ymin=0.05, ymax=0.35, colors='tomato', alpha=0.6, linestyles='--', label=f'% Mulheres: {100*TX_GEN_FEMININO:.0f}%')

plt.legend()

handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[12:]
labels = labels[12:]  

plt.legend(handles=handles, labels=labels)

plt.savefig('../img/partidos_cor_raca_genero_clusterbr.png')
# %%
