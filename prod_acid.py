import numpy as np
import pandas as pd

# Leitura dos dados de Produção em TU e TKU
Producao = pd.read_excel('Producao.xlsx')

# Leitura dos dados de Acidentes
Acidentes = pd.read_excel('Registro_de_Acidentes.xlsx')

# Leitura dos dados de Indice de Acidentes
Indice_Acidentes = pd.read_excel('Indice de Acidentes.xlsx')

# Introdução de grupo Total com a soma de todas as TKUs e TUs
meses = Producao['Mes/Ano'].unique()

for i in meses:
    filtro1 = Producao['Mes/Ano'] == i
    prod_filt = Producao[filtro1]

    soma_tu = sum(prod_filt['TU'])
    soma_tku = sum(prod_filt['TKU'])

    row_ins = [i, 'Total', soma_tu, soma_tu*1000000, soma_tku, soma_tku*1000000000]
    row_df = pd.DataFrame([row_ins], columns=['Mes/Ano', 'Ferrovia', 'TU', 'Tuinicial', 'TKU', 'TKUinicial'])
    Producao = pd.concat([row_df, Producao], ignore_index=True)

# Introdução de grupo Total com a soma dos Acidentes
anos = Acidentes['Ano'].unique()

for i in anos:
    filtro1 = Acidentes['Ano'] == i
    acid_filt = Acidentes[filtro1]

    soma_acid = sum(acid_filt['Acidentes'])

    row_ins = ['Total', i, soma_acid]
    row_df = pd.DataFrame([row_ins], columns=['Ferrovia', 'Ano', 'Acidentes'])
    Acidentes = pd.concat([row_df, Acidentes], ignore_index=True)