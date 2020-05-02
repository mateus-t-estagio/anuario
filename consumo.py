import pandas as pd
import numpy as np
from prod_acid import Producao

tblAbastecimento = pd.read_excel('tblAbastecimento.xlsx')
tblDesempenhoLocomotiva = pd.read_excel('tblDesempenhoLocomotiva.xlsx')
tblFerrovia = pd.read_csv('tblFerrovia.csv', sep=';', decimal=',')
tblFerrovia = tblFerrovia[['CodigoFerrovia', 'SiglaFerrovia']]

tblAbastecimento = tblAbastecimento.merge(tblFerrovia, on = 'CodigoFerrovia')
tblAbastecimento['Consumo'] = tblAbastecimento['LitrosManobra'] + tblAbastecimento['LitrosViagem'] + tblAbastecimento['LitrosOutro']
tblAbastecimento = tblAbastecimento[['SiglaFerrovia', 'DataReferencia', 'Consumo']]

filtro1 = tblAbastecimento['DataReferencia'] != '01/01/2020 00:00:00'
tblAbastecimento = tblAbastecimento[filtro1]
filtro2 = tblAbastecimento['DataReferencia'] != '01/02/2020 00:00:00'
tblAbastecimento = tblAbastecimento[filtro2]
filtro3 = tblAbastecimento['DataReferencia'] != '01/03/2020 00:00:00'
tblAbastecimento = tblAbastecimento[filtro3]

new = tblAbastecimento['DataReferencia'].str.split(" ", n=1, expand=True)
tblAbastecimento['DataReferencia'] = new[0]


tblDesempenhoLocomotiva = tblDesempenhoLocomotiva.merge(tblFerrovia, on = 'CodigoFerrovia')
tblDesempenhoLocomotiva = tblDesempenhoLocomotiva[['SiglaFerrovia', 'DataReferencia', 'NumeroConsumoCombustivel']]

filtro1 = tblDesempenhoLocomotiva['DataReferencia'] != '01/01/2020 00:00:00'
tblDesempenhoLocomotiva = tblDesempenhoLocomotiva[filtro1]
filtro2 = tblDesempenhoLocomotiva['DataReferencia'] != '01/02/2020 00:00:00'
tblDesempenhoLocomotiva = tblDesempenhoLocomotiva[filtro2]
filtro3 = tblDesempenhoLocomotiva['DataReferencia'] != '01/03/2020 00:00:00'
tblDesempenhoLocomotiva = tblDesempenhoLocomotiva[filtro3]

new1 = tblDesempenhoLocomotiva['DataReferencia'].str.split(" ", n=1, expand=True)
tblDesempenhoLocomotiva['DataReferencia'] = new1[0]
tblAbastecimento['Consumo'] = tblAbastecimento['Consumo']/1000000
tblDesempenhoLocomotiva['NumeroConsumoCombustivel'] = tblDesempenhoLocomotiva['NumeroConsumoCombustivel']/1000000

tblDesempenhoLocomotiva['DataReferencia'] = pd.to_datetime(tblDesempenhoLocomotiva['DataReferencia'], format='%d/%m/%Y')
tblAbastecimento['DataReferencia'] = pd.to_datetime(tblAbastecimento['DataReferencia'], format='%d/%m/%Y')

tblDesempenhoLocomotiva = tblDesempenhoLocomotiva.sort_values(by='DataReferencia', axis=0)
tblAbastecimento = tblAbastecimento.sort_values(by='DataReferencia', axis=0)

tblDesempenhoLocomotiva['Consumo'] = tblDesempenhoLocomotiva['NumeroConsumoCombustivel']

tblDesempenhoLocomotivai = pd.pivot_table(tblDesempenhoLocomotiva,
                                          values='Consumo', 
                                          index=['SiglaFerrovia', 'DataReferencia'], 
                                          aggfunc=np.sum)
tblDesempenhoLocomotiva = pd.DataFrame(tblDesempenhoLocomotivai.to_records())

tblAbastecimentoi = pd.pivot_table(tblAbastecimento, 
                                   values='Consumo',
                                   index=['SiglaFerrovia', 'DataReferencia'],
                                   aggfunc=np.sum)
tblAbastecimento = pd.DataFrame(tblAbastecimentoi.to_records())

meses = tblAbastecimento['DataReferencia'].unique()

for i in meses:
    filtro1 = tblAbastecimento['DataReferencia'] == i
    ab_filt = tblAbastecimento[filtro1]

    soma_cons = sum(ab_filt['Consumo'])

    row_ins = ['Total', i, soma_cons]
    row_df = pd.DataFrame([row_ins], columns=['SiglaFerrovia', 'DataReferencia', 'Consumo'])
    tblAbastecimento = pd.concat([row_df, tblAbastecimento], ignore_index=True)

meses = tblDesempenhoLocomotiva['DataReferencia'].unique()

for i in meses:
    filtro1 = tblDesempenhoLocomotiva['DataReferencia'] == i
    ab_filt = tblDesempenhoLocomotiva[filtro1]

    soma_cons = sum(ab_filt['Consumo'])

    row_ins = ['Total', i, soma_cons]
    row_df = pd.DataFrame([row_ins], columns=['SiglaFerrovia', 'DataReferencia', 'Consumo'])
    tblDesempenhoLocomotiva = pd.concat([row_df, tblDesempenhoLocomotiva], ignore_index=True)

Producao['Mes/Ano'] = pd.to_datetime(Producao['Mes/Ano'], format='%m/%Y')

tblAbastecimento['Ferrovia'] = tblAbastecimento['SiglaFerrovia']
tblAbastecimento['Mes/Ano'] = tblAbastecimento['DataReferencia']

tblAbastecimentoN = tblAbastecimento.merge(Producao, on = ['Ferrovia', 'Mes/Ano'])

tblAbastecimentoN['Consumo_Relativo'] = tblAbastecimentoN['Consumo']/(tblAbastecimentoN['TKU'])

tblAbastecimentoN = tblAbastecimentoN[['Ferrovia', 'Mes/Ano', 'Consumo_Relativo']]

tblAbastecimento = tblAbastecimento.merge(tblAbastecimentoN, on=['Ferrovia', 'Mes/Ano'])



tblDesempenhoLocomotiva['Ferrovia'] = tblDesempenhoLocomotiva['SiglaFerrovia']
tblDesempenhoLocomotiva['Mes/Ano'] = tblDesempenhoLocomotiva['DataReferencia']

tblDesempenhoLocomotivaN = tblDesempenhoLocomotiva.merge(Producao, on = ['Ferrovia', 'Mes/Ano'])

tblDesempenhoLocomotivaN['Consumo_Relativo'] = tblDesempenhoLocomotivaN['Consumo']/(tblDesempenhoLocomotivaN['TKU'])

tblDesempenhoLocomotivaN = tblDesempenhoLocomotivaN[['Ferrovia', 'Mes/Ano', 'Consumo_Relativo']]

tblDesempenhoLocomotiva = tblDesempenhoLocomotiva.merge(tblDesempenhoLocomotivaN, on=['Ferrovia', 'Mes/Ano'])