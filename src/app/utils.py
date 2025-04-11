# %%
import matplotlib.pyplot as plt
import seaborn as sn
from adjustText import adjust_text
from sklearn import cluster


# %%

def make_scatter(data, cluster=False, size=False):

    config = {
        'data': data, 
        'x': 'TX_GEN_FEMININO', 
        'y': 'TX_COR_RACA_PRETA',
        'size': 'TOTAL_CANDIDATURAS',
        'sizes': (5,300),
        'hue': 'cluster',
        'palette': 'viridis',
        'alpha': 0.6,
    }

    if not cluster:
        del config['hue']
        del config['palette']

    if not size:
        del config['size']
        del config['sizes']

    fig = plt.figure(dpi=360, figsize=(6,5.5))

    sn.scatterplot(**config)

    texts = []
    for i in data['SG_PARTIDO']:
        data_tmp = data[data['SG_PARTIDO'] == i]
        x = data_tmp['TX_GEN_FEMININO'].values[0]
        y = data_tmp['TX_COR_RACA_PRETA'].values[0]
        texts.append(plt.text(x, y, i, fontsize=9))

    adjust_text(texts, only_move={'points': 'y', 'texts': 'y'}, arrowprops=dict(arrowstyle="-"))

    plt.grid(True)
    plt.suptitle('Partidos: Cor vs Gênero - Eleições 2024')

    if size:
        plt.title('Tamanho bolha = Qtde. Candidatos do Partido', fontdict={'size': 9})
    
    plt.xlabel('Taxa de Mulheres')
    plt.ylabel('Taxa de Pessoas Pretas')

    TX_COR_RACA_PRETA = data['TOTAL_COR_RACA_PRETA'].sum() / data['TOTAL_CANDIDATURAS'].sum()
    TX_GEN_FEMININO = data['TOTAL_GEN_FEMININO'].sum() / data['TOTAL_CANDIDATURAS'].sum()

    plt.hlines(y=TX_COR_RACA_PRETA,
               xmin=data['TX_GEN_FEMININO'].min(),
               xmax=data['TX_GEN_FEMININO'].max(),
               colors='black',
               alpha=0.6,
               linestyles='--',
               label=f'% Pessoas Pretas: {100*TX_COR_RACA_PRETA:.0f}%'
               )


    plt.vlines(x=TX_GEN_FEMININO,
               ymin=data['TX_COR_RACA_PRETA'].min(),
               ymax=data['TX_COR_RACA_PRETA'].max(),
               colors='tomato',
               alpha=0.6,
               linestyles='--',
               label=f'% Mulheres: {100*TX_GEN_FEMININO:.0f}%'
               )

    plt.legend()

    handles, labels = plt.gca().get_legend_handles_labels()
    handles = handles[-2:]
    labels = labels[-2:]  

    plt.legend(handles=handles, labels=labels)

    return fig

def make_clusters(data, n=6):
    model = cluster.KMeans(n_clusters=n, random_state=42, max_iter=1000)
    model.fit(data[['TX_GEN_FEMININO', 'TX_COR_RACA_PRETA']])
    data['cluster'] = model.labels_
    return data
