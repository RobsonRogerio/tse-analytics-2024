
import json
import pandas as pd
import sqlalchemy

caminho_json = '../src/ingestoes.json'

engine = sqlalchemy.create_engine('sqlite:///../data/database.db')

with open(caminho_json, 'r') as open_file:
    ingestoes = json.load(open_file)

for i in ingestoes:
    path = i['path']
    df = pd.read_csv(path, encoding='latin-1', sep=';')
    df.to_sql(i['table'], engine, if_exists='replace', index=False)






