from dash import dash, html, dash_table, dcc, Input, Output, State
from app import *
from connection_lab import *
from pages import navbar
from datetime import datetime
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc
import pandas as pd

card_style = {
    "width": "100%",
    "height": "100%",
    'padding': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}

card_style2 = {
    "width": "45%",
    "height": "100%",
    'padding': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}

df = pd.DataFrame(pd.read_sql("SELECT * FROM LABORATORIO", conn))
df_data = df.loc[:, ["DATA"]]
menor_data = datetime.strptime(str(df_data["DATA"].min()), "%Y-%m-%d %H:%M:%S")
menor_dia, menor_mes, menor_ano = menor_data.day, menor_data.month, menor_data.year
maior_data = datetime.strptime(str(df_data["DATA"].max()), "%Y-%m-%d %H:%M:%S")
maior_dia, maior_mes, maior_ano = maior_data.day, maior_data.month, maior_data.year


content = html.Div([

    dbc.Row([
        dbc.Card([
            html.Legend("Filtro por data"),
            dcc.DatePickerSingle(id="datepicker_lab", display_format="DD/MM/YYYY", min_date_allowed=menor_data, max_date_allowed=maior_data, date=maior_data, style={"margin-bottom": "5px"}),
            dcc.Dropdown(id="dropdown_colunas_lab", options=[i for i in df.columns], multi=True, placeholder="Colunas", value=["DATA", "CODIGO"]),
            
        ], style={"width": "45%","height": "100%",'padding': '25px','align-self': 'center','display': 'flex','flex-direction': 'column', "justify-content": "center", 'margin-right': '5%'}),

        dbc.Card([
            html.Legend("Funções"),
            dbc.Row([
                dbc.Button("Adicionar registro", id="add_registro_lab", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Adicionar coluna", id="add_coluna_lab", style={"margin": "2px", "width": "40%"}),
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),
            dbc.Row([
                dbc.Button("Atualizar registro", id="update_registro_lab", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Excluir registro", id="exc_registro_lab", style={"margin": "2px", "width": "40%"})
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),
            dbc.Row([
                dbc.Button("Exportar dados", id="export_planilha", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Remover coluna", id="remove_coluna_lab", style={"margin": "2px", "width": "40%"})
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),
            dbc.Row([
                dcc.Checklist(["Editável"], id="editable_check", inline=True),
                dcc.Checklist(["Selecionável"], id="selectable_check", inline=True)
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"})
            
        ], style={"width": "45%","height": "100%",'padding': '25px','align-self': 'center','display': 'flex','flex-direction': 'column', 'margin-left': '5%'})
    ], style={"height": "40%", "width": "80%", "margin": "10px", "display": "flex", "flex-direction": "row", "justify-content": "center"}),

    dbc.Row([
        dbc.Card([
            html.Legend("Tabela MPAES"),
            dash_table.DataTable(id="tabela_lab", data=[{}], style_table={"height": '300px', 'overflowY': 'auto'}, editable=False, style_cell={"textAlign": "left"}, style_header={"fontWeight": "bold"}, style_as_list_view=False)
        ],style=card_style)
    ], style={"height": "55%", "width": "80%", "margin": "10px"}),

], style={"display": 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'})



def render_layout(user):
    username = user.nm_usr

    layout = html.Div([
        dcc.Location(id="lab_mpaes_url", refresh=True),
        dcc.Download(id="download"),
        navbar.nav()[0],
            dbc.Row([   
                content
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return layout

@app.callback(
    Output("tabela_lab", "data"),
    Output("tabela_lab", "columns"),
    Input("datepicker_lab", "date"),
    Input("dropdown_colunas_lab", "value")
)
def preencher_tabela(data, colunas):
    df_filtrado = pd.DataFrame(pd.read_sql(f"SELECT * FROM LABORATORIO WHERE CAST(DATA AS DATE) = '{data}'", conn))

    if len(colunas) != 0:
        df_filtrado = df_filtrado.loc[:, [ str(col) for col in colunas ]]

    values = df_filtrado.to_dict(orient="records")
    cols = [ {"name": str(col), "id": str(col)} for col in df_filtrado.columns ]

    return [ values, cols ]

@app.callback(
    Output("tabela_lab", "row_selectable"),
    Input("selectable_check", "value"),
)
def ativar_selectable(value):
    # if(value is None) or (len(value)==0):
    #     return None
    # else:
    #     return "single"
   return None if((value is None) or (len(value)==0)) else "single"
@app.callback(
    Output("tabela_lab", "editable"),
    Input("editable_check", "value")
)
def ativar_editable(value):
    # if(value is None) or (len(value)==0):
    #     return False
    # else:
    #     return True
    return False if((value is None) or (len(value)==0)) else True

@app.callback(
    Output("download", "data"),
    Input("export_planilha", "n_clicks"),
    State("tabela_lab", "data"),
    State("datepicker_lab", "date"),
    State("dropdown_colunas_lab", "value"),
    prevent_initial_call=True
)
def exportar_planilha(n, dados, filtro_data, filtro_colunas):
    if n is None:
        raise PreventUpdate
    else:
        df_filtrado = pd.DataFrame(pd.read_sql(f"SELECT * FROM LABORATORIO WHERE CAST(DATA AS DATE) = '{filtro_data}'", conn))

        if len(filtro_colunas) != 0:
            df_filtrado = df_filtrado.loc[:, [ str(col) for col in filtro_colunas ]]

        return dcc.send_data_frame(df_filtrado.to_excel, "dados.xlsx", sheet_name="LABORATORIO_MPAES")