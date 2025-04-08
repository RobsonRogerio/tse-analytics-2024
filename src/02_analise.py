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
plt.figure(dpi=400)

sn.scatterplot(data=df, 
               x='TX_GEN_FEM_BR', 
               y='TX_COR_RACA_PRETA_BR')

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

plt.hlines(y=TX_COR_RACA_PRETA, xmin=0.30, xmax=0.55, colors='black', linestyles='--', label=f'% Candidaturas Pessoas Pretas: {100*TX_COR_RACA_PRETA:.0f}%')
plt.vlines(x=TX_GEN_FEMININO, ymin=0.05, ymax=0.35, colors='tomato', linestyles='--', label=f'% Candidaturas Mulheres: {100*TX_GEN_FEMININO:.0f}%')

plt.legend()

plt.savefig('../img/partidos_cor_raca_genero.png')

# %%
