"""
Código para o Dashboard do Anuário Estatístico
Líder do Projeto - Thiago de Oliveira Victorino - thiago.victorino@antt.gov.br
Colaborador - Mateus Tiago de Oliveira - mateus.estagio-o@antt.gov.br

"""


import warnings
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
#from prod_acid import Producao, Acidentes, Indice_Acidentes
#from consumo import tblAbastecimento, tblDesempenhoLocomotiva

warnings.filterwarnings("ignore")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server

# Listas para os callbacks e dropdowns
Ferrovias = ['Total', 'EFC', 'EFVM', 'FTC', 'FTL', 'FCA', 'RMN', 'RMP', 'RMO', 'RMS', 'MRS', 'EFPO', 'FNSTN']
TU_TKU = ['TU', 'TKU']
lConsumo = ['Consumo', 'Abastecimento']
esc_aci = ['Total de Acidentes','Índice de Acidentes']
colors = {'text':'#000000'}


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











# Definição do layout da página
app.layout=html.Div([
    dcc.Tabs([
        # Primeira Tab com os dados de Produção e Segurança
        dcc.Tab(label='Produção e Segurança', children=[
                html.H2(children='Produção de Transporte ',style={
                    'textAlign': 'center',
                    'color': colors['text']}),

                html.Label(children='Ferrovias:'),
                dcc.Dropdown(
                            id='id_dropdown_ferr',
                            options=[{'label': i, 'value': i} for i in Ferrovias],
                            value=['Total'],
                            multi=True),
                dcc.RadioItems(
                            id='id_radio_TON',
                            options=[{'label': i, 'value': i} for i in TU_TKU],
                            value='TU',
                            labelStyle={'display': 'inline-block'}
                        ),
                html.Div([dcc.Graph(id='grafico_producao')]), 

                html.H2(children='Segurança',style={
                    'textAlign': 'center',
                    'color': colors['text']}),            

                html.Label(children='Ferrovias:'),
                dcc.Dropdown(
                            id='id_dropdown_acidente',
                            options=[{'label': i, 'value': i} for i in Ferrovias],
                            value=['Total'],
                            multi=True),
                dcc.RadioItems(
                            id='id_radio_acidente',
                            options=[{'label': i, 'value': i} for i in esc_aci],
                            value='Total de Acidentes',
                            labelStyle={'display': 'inline-block'}),
                
                        html.Div([dcc.Graph(id='grafico_acidentes')])  
        ]), # Fim da primeira Tab

        # Tab de desempenho de trem (consumo e material rodante)
        dcc.Tab(label='Consumo e Abastecimento', children=[
                html.H2(children='Consumo e Abastecimento de Combustível ',style={
                    'textAlign': 'center',
                    'color': colors['text']}),

                html.Div([
                    html.Label(children='Ferrovias:'),
                    dcc.Dropdown(
                                id='id_dropdown_consumo',
                                options=[{'label': i, 'value': i} for i in Ferrovias],
                                value=['Total'],
                                multi=True),
                    dcc.RadioItems(
                                id='id_radio_abast',
                                options=[{'label': i, 'value': i} for i in lConsumo],
                                value='Consumo'),
                    html.Div([dcc.Graph(id='grafico_consumo')]), 
                ]),
                html.H2(children='Consumo e Abastecimento Relativo de Combustível ',style={
                    'textAlign': 'center',
                    'color': colors['text']}),

                html.Div([
                html.Label(children='Ferrovias:'),
                    dcc.Dropdown(
                                id='id_dropdown_consumo_relativo',
                                options=[{'label': i, 'value': i} for i in Ferrovias],
                                value=['Total'],
                                multi=True),
                    dcc.RadioItems(
                                id='id_radio_abast1',
                                options=[{'label': i, 'value': i} for i in lConsumo],
                                value='Consumo'),
                    html.Div([dcc.Graph(id='grafico_consumo1')]),                 
                ]),

        ]) # Fim da segunda tab

    ]) # Fim do dcc.Tabs

]) # Fim do html.Div principal

# Calbacks para os gráficos
@app.callback(dash.dependencies.Output('grafico_producao','figure'),[
        dash.dependencies.Input('id_dropdown_ferr','value'),
        dash.dependencies.Input('id_radio_TON','value')
    ])
def prod_transporte(x_ferr,y_tu):
    
    if y_tu == 'TU':
        unidade = 'Milhões de '
    else:
        unidade = 'Bilhões de '

    # Lista com as ferrovias escolhidas no dropdown 
    Ferr_Select=x_ferr
    # Dicionário onde serão salvos os DataFrames referentes a cada Ferrovia   
    Ferrovia_to_Analise= {}
    # Loop para filtrar os dados referentes a cada ferrovia 
    for val in Ferr_Select:
        #Filtrar os dados referente a Ferrovia na lista Ferr_Select
        iProducao=Producao['Ferrovia']==val
        Ferrovia_Escolhida=Producao[iProducao]
        Ferrovia_Escolhida['Mes/Ano']=pd.to_datetime(Ferrovia_Escolhida['Mes/Ano'])
        #Salvando no espaço val o DataFrame referente a Ferrovia em Ferr_Select
        Ferrovia_to_Analise[val]=Ferrovia_Escolhida    
    df=pd.DataFrame()
    trace={}
    tracado=[]
    #Loop para manipular e salvar os dados para a criação dos gráficos
    for val in Ferr_Select:
        #Base de dados para a Ferrovia em Ferr_Select 
        df=Ferrovia_to_Analise[val]
        #Lista de dados do eixo x
        x=df['Mes/Ano']
        #Lista de dados do eixo y
        y=df[y_tu]
        #Traçado referente a cada Ferrovia em Ferr_Select
        trace[val] = go.Scatter(x=x,
                            y=y,
                            mode='lines+markers',
                            name=val) 
        #Lista acumulando as informações de cada gráfico
        tracado.append(trace[val]) 
    data=tracado
    #Formatando a lista de Ferrovias para colocar no titulo do gráfico
    z=', '.join(x_ferr) 
    #Criação dos gráficos  
    return {
            'data': data,
            'layout': {
            'title':'Produção de Transporte - Ferrovia: ' + z,
            'xaxis':{'title': 'Ano'},
            'yaxis':{'title': unidade + y_tu },
            }}

@app.callback(dash.dependencies.Output('grafico_acidentes','figure'),[
        dash.dependencies.Input('id_dropdown_acidente','value'),
        dash.dependencies.Input('id_radio_acidente','value')
    ])
def numero_acidentes(x_ferr,y_tu):
    #Condição para a seleção do tipo de informação, referente ou ao total de acidentes ou aos indices de acidentes
    if y_tu == 'Total de Acidentes':
        #Criando a lista com as informações escolhidas pelo usuário no dropdown
        Ferr_Select=x_ferr
        Ferrovia_to_Analise = {}
        #Loop para filtrar os dados referentes a cada ferrovia 
        for val in Ferr_Select:
        #Filtrar os dados referente a Ferrovia na lista Ferr_Select
            Ferrovia=Acidentes
            iFerrovia=Ferrovia['Ferrovia']==val
            Ferrovia_Escolhida=Ferrovia[iFerrovia]
            Ferrovia_to_Analise[val]=Ferrovia_Escolhida
        df=pd.DataFrame()
        trace={}
        tracado=[]
        for val in Ferr_Select:
            #Criando DataFrame referente aos dados de cada Ferrovia
            df=Ferrovia_to_Analise[val]
            #Definindo os parâmetros x e y do gráfifo 
            x=df['Ano']
            y=df['Acidentes']
            #Criando o gráfico da Ferrovia "val"
            trace[val]=go.Bar(x=x,
                                y=y,
                                text='Número de Acidentes',
                                name=val)
            #Agrupando um conjunto de base de dados referente a cada Ferrovia em Ferr_Select
            #Uma lista salvando cada conjunto de traçados de gráficos em "trace[val]"
            tracado.append(trace[val])
        data=tracado
        #Formatando a lista de Ferrovias para colocar no titulo do gráfico
        z=', '.join(x_ferr) 
        #Criação dos gráficos 
        return {
                'data': data,
                'layout': {
                'title':'Número de Acidentes - Ferrovia: '+ z,
                'xaxis':{'title': 'Ano'},
                'yaxis':{'title': 'N° de Acidentes'},
                }}
    else:
        #Criando a lista com as informações escolhidas pelo usuário no dropdown
        Ferr_Select=x_ferr
        #Criando as listas e dicionários que serão utilizado no decorrer do código
        Ferrovia_to_Analise = {}
        Ferrovia=pd.DataFrame()
        trace={}
        tracado=[]
        for val in Ferr_Select:
            #Escolhendo a base de dados a partir da qual serão realizadas as manipulações e criações de gráfico
            Ferrovia=Indice_Acidentes
            iFerrovia=Ferrovia['Concessionária']==val
            Ferrovia=Ferrovia[iFerrovia]
            #Definindo os parâmetros x e y do gráfifo
            x=Ferrovia['Ano']
            y=Ferrovia['Realizado']
            #Criando o gráfico da Ferrovia "val"
            trace[val]=go.Bar(x=x,
                                y=y,
                                text='Índice de Acidentes',
                                name=val)
            tracado.append(trace[val])
        #Agrupando um conjunto de base de dados referente a cada Ferrovia em Ferr_Select
        #Uma lista salvando cada conjunto de traçados de gráficos em "trace[val]"
        data=tracado

        #Formatando a lista de Ferrovias para colocar no titulo do gráfico
        z=', '.join(x_ferr) 
        #Criação dos gráficos  
        return {
                'data': data,
                'layout': {
                'title':'Índice de Acidentes - Ferrovia: ' + z,
                'xaxis':{'title': 'Ano'},
                'yaxis':{'title': 'Indice de Acidentes'},
                }}

@app.callback(dash.dependencies.Output('grafico_consumo','figure'),[
        dash.dependencies.Input('id_dropdown_consumo','value'),
        dash.dependencies.Input('id_radio_abast','value')
    ])
def consumo(x_ferr,y_c):
    
    if y_c == 'Consumo':
        df_comb = tblDesempenhoLocomotiva
    else:
        df_comb = tblAbastecimento

    # Lista com as ferrovias escolhidas no dropdown 
    Ferr_Select = x_ferr
    # Dicionário onde serão salvos os DataFrames referentes a cada Ferrovia   
    Ferrovia_to_Analise = {}
    # Loop para filtrar os dados referentes a cada ferrovia 
    for val in Ferr_Select:
        #Filtrar os dados referente a Ferrovia na lista Ferr_Select
        icons=df_comb['SiglaFerrovia']==val
        Ferrovia_Escolhida=df_comb[icons]
        #Ferrovia_Escolhida['DataReferencia']=pd.to_datetime(Ferrovia_Escolhida['DataReferencia'], format='%d/%m/%Y')
        #Salvando no espaço val o DataFrame referente a Ferrovia em Ferr_Select
        Ferrovia_to_Analise[val]=Ferrovia_Escolhida    
    df=pd.DataFrame()
    trace={}
    tracado=[]
    #Loop para manipular e salvar os dados para a criação dos gráficos
    for val in Ferr_Select:
        #Base de dados para a Ferrovia em Ferr_Select 
        df=Ferrovia_to_Analise[val]
        #Lista de dados do eixo x
        x=df['DataReferencia']
        #Lista de dados do eixo y
        y=df['Consumo']
        #Traçado referente a cada Ferrovia em Ferr_Select
        trace[val] = go.Scatter(x=x,
                            y=y,
                            mode='lines+markers',
                            name=val) 
        #Lista acumulando as informações de cada gráfico
        tracado.append(trace[val]) 
    data=tracado

    #Formatando a lista de Ferrovias para colocar no titulo do gráfico
    z=', '.join(x_ferr) 
    #Criação dos gráficos  
    return {
            'data': data,
            'layout': {
            'title':'Consumo e Abastecimento de Combustível - Ferrovia: ' + z,
            'xaxis':{'title': 'Ano'},
            'yaxis':{'title': 'Milhões de Litros'},
            }}

@app.callback(dash.dependencies.Output('grafico_consumo1','figure'),[
        dash.dependencies.Input('id_dropdown_consumo_relativo','value'),
        dash.dependencies.Input('id_radio_abast1','value')
    ])
def consumo_relativo(x_ferr,y_c):
    
    if y_c == 'Consumo':
        df_comb = tblDesempenhoLocomotiva
    else:
        df_comb = tblAbastecimento

    # Lista com as ferrovias escolhidas no dropdown 
    Ferr_Select = x_ferr
    # Dicionário onde serão salvos os DataFrames referentes a cada Ferrovia   
    Ferrovia_to_Analise = {}
    # Loop para filtrar os dados referentes a cada ferrovia 
    for val in Ferr_Select:
        #Filtrar os dados referente a Ferrovia na lista Ferr_Select
        icons=df_comb['SiglaFerrovia']==val
        Ferrovia_Escolhida=df_comb[icons]
        #Ferrovia_Escolhida['DataReferencia']=pd.to_datetime(Ferrovia_Escolhida['DataReferencia'], format='%d/%m/%Y')
        #Salvando no espaço val o DataFrame referente a Ferrovia em Ferr_Select
        Ferrovia_to_Analise[val]=Ferrovia_Escolhida    
    df=pd.DataFrame()
    trace={}
    tracado=[]
    #Loop para manipular e salvar os dados para a criação dos gráficos
    for val in Ferr_Select:
        #Base de dados para a Ferrovia em Ferr_Select 
        df=Ferrovia_to_Analise[val]
        #Lista de dados do eixo x
        x=df['DataReferencia']
        #Lista de dados do eixo y
        y=df['Consumo_Relativo']
        #Traçado referente a cada Ferrovia em Ferr_Select
        trace[val] = go.Scatter(x=x,
                            y=y,
                            mode='lines+markers',
                            name=val) 
        #Lista acumulando as informações de cada gráfico
        tracado.append(trace[val]) 
    data=tracado

    #Formatando a lista de Ferrovias para colocar no titulo do gráfico
    z=', '.join(x_ferr) 
    #Criação dos gráficos  
    return {
            'data': data,
            'layout': {
            'title':'Consumo e Abastecimento Relativo de Combustível - Ferrovia: ' + z,
            'xaxis':{'title': 'Ano'},
            'yaxis':{'title': 'Litros por Milhares de TKU'},
            }}

if __name__ == '__main__':
    app.run_server()
