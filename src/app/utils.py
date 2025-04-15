# %%
import matplotlib.pyplot as plt
import seaborn as sn
from adjustText import adjust_text
from sklearn import cluster
from sklearn import preprocessing


# %%

def make_scatter(data, x, y, x_label, y_label, cluster=False, size=False):

    config = {
        'data': data, 
        'x': x, 
        'y': y,
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
        x_pos = data_tmp[x].values[0]
        y_pos = data_tmp[y].values[0]
        texts.append(plt.text(x_pos, y_pos, i, fontsize=9))

    adjust_text(texts, only_move={'points': 'y', 'texts': 'y'}, arrowprops=dict(arrowstyle="-"))

    plt.grid(True)
    plt.suptitle(f'{x_label.title()} vc {y_label.title()} - Eleições 2024')

    if size:
        plt.title('Tamanho bolha = Qtde. Candidatos do Partido', fontdict={'size': 9})
    
    plt.xlabel(x_label.title())
    plt.ylabel(y_label.title())

    if x == 'TX_GEN_FEMININO' and y == 'TX_COR_RACA_PRETA':
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

    else:
        legend = plt.legend()
        legend.remove()

    return fig

def make_clusters(data, features, n=6):
    norm = preprocessing.MinMaxScaler()
    data_norm = norm.fit_transform(data[features])
    model = cluster.KMeans(n_clusters=n, random_state=42, max_iter=10000)
    model.fit(data_norm)
    data['cluster'] = model.labels_
    return data
