from dash import dash, html, dash_table, dcc, Input, Output, State
from app import *
from connection_lab import *
from pages import navbar
from datetime import datetime
from sqlalchemy import text

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

df = pd.DataFrame(pd.read_sql("select * from LABORATORIO_RAIOX", conn))
df_data = df.loc[:, ["DATA"]]
menor_data = datetime.strptime(str(df_data["DATA"].min()), "%Y-%m-%d %H:%M:%S")
maior_data = datetime.strptime(str(df_data["DATA"].max()), "%Y-%m-%d %H:%M:%S")

content = html.Div([

    dbc.Row([

        dbc.Card([
            html.Legend("Filtro por data"),
            dcc.DatePickerSingle(id="datepicker_lab_raiox", display_format="DD/MM/YYYY", min_date_allowed=menor_data, max_date_allowed=maior_data, date=maior_data, style={"margin-bottom": "5px"}),
            dcc.Dropdown(id="dropdown_colunas_lab_raiox", options=[ col for col in df.columns ], multi=True, placeholder="Colunas", value=["CODIGO_AMOSTRA", "DATA"])

        ], style={"width": "45%","height": "100%",'padding': '25px','align-self': 'center','display': 'flex','flex-direction': 'column', "justify-content": "center", 'margin-right': '5%'}),

        dbc.Card([

            html.Legend("Funções"),

            dbc.Row([

                dbc.Button("Adicionar registro", id="add_registro_lab_raiox", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Adicionar coluna", id="add_coluna_lab_raiox", style={"margin": "2px", "width": "40%"}),

            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),

            dbc.Row([

                dbc.Button("Atualizar registro", id="update_registro_lab_raiox", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Excluir registro", id="exc_registro_lab_raiox", style={"margin": "2px", "width": "40%"}),

            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),

            dbc.Row([

                dbc.Button("Exportar dados", id="export_planilha_raiox", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Remover coluna", id="remove_coluna_raiox", style={"margin": "2px", "width": "40%"}),

            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),

            dbc.Row([

                dcc.Checklist([" Editável"], id="editable_check_raiox", inline=True),
                dcc.Checklist([" Selecionável"], id="selectable_check_raiox", inline=True),

            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),

        ], style={"width": "45%","height": "100%",'padding': '25px','align-self': 'center','display': 'flex','flex-direction': 'column', "justify-content": "center", 'margin-left': '5%'}),

    ], style={"height": "40%", "width": "80%", "margin": "10px", "display": "flex", "flex-direction": "row", "justify-content": "center"}),

    dbc.Row([

        dbc.Card([

            html.Legend("Tabela Raio-X"),

            dash_table.DataTable(id="tabela_lab_raiox", data=[{}], style_table={"height": "300px", "overflowY": "auto"}, editable=False, style_cell={"textAlign": "left"}, style_header={"fontWeight": "bold"}, style_as_list_view=False)

        ], style=card_style)

    ], style={"height": "55%", "width": "80%", "margin": "10px"})

], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "align-items": "center"})

def render_layout(user):
    username = user.nm_usr

    layout = html.Div([
        dcc.Location(id="lab_raiox_url", refresh=True),
        dcc.Download(id="download_raiox"),

        # Seções de modais
        # ================================

        dbc.Modal([

            dbc.ModalHeader(dbc.ModalTitle("Criar nova coluna")),
            
            dbc.ModalBody([

                dbc.Input(id="nome_coluna_add_coluna_raiox", placeholder="Nome da nova coluna", style={"margin-bottom": "5px"}),

                dcc.Dropdown(id="tipo_coluna_add_coluna_raiox", options=["Data", "Texto", "Número"], placeholder="Tipo de dado")

            ]),

            dbc.ModalFooter([

                dbc.Button("Fechar", id="fechar_modal_add_coluna_raiox", class_name="ms-auto"),

                dbc.Button("Adicionar", id="botao_add_coluna_raiox", class_name="ms-auto")

            ])

        ], id="modal_add_coluna_raiox", is_open=False),

        dbc.Modal([

            dbc.ModalHeader(dbc.ModalTitle("Remover colunas")),

            dbc.ModalBody([
                dcc.Dropdown(id="coluna_remover_raiox", options=[], multi=True)
            ]),

            dbc.ModalFooter([

                dbc.Button("Fechar", id="fechar_modal_remove_coluna_raiox", class_name="ms-auto"),

                dbc.Button("Remover", id="botao_remove_coluna_raiox", class_name="ms-auto")

            ])

        ], id="modal_remove_coluna_raiox", is_open=False),

        # ================================

        navbar.nav()[0],
            dbc.Row([   
                content
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return layout

@app.callback(
    Output("tabela_lab_raiox", "data"),
    Output("tabela_lab_raiox", "columns"),
    Input("datepicker_lab_raiox", "date"),
    Input("dropdown_colunas_lab_raiox", "value")
)
def preencher_tabela_raiox(data, colunas):
    df_filtrado = pd.DataFrame(pd.read_sql(f"SELECT * FROM LABORATORIO_RAIOX WHERE CAST(DATA AS DATE) = '{data}'", conn))

    if len(colunas) != 0:
        df_filtrado = df_filtrado.loc[:, [ str(col) for col in colunas ]]

    values = df_filtrado.to_dict(orient="records")
    cols = [ {"name": str(col), "id": str(col)} for col in df_filtrado.columns ]

    return [ values, cols ]

@app.callback(
    Output("tabela_lab_raiox", "row_selectable"),
    Input("selectable_check_raiox", "value")
)
def ativar_selectable_raiox(value):
    return None if((value is None) or (len(value)==0)) else "single"

@app.callback(
    Output("tabela_lab_raiox", "editable"),
    Input("editable_check_raiox", "value")
)
def ativar_selectable_raiox(value):
    return False if ((value is None) or (len(value)==0)) else True

@app.callback(
    Output("download_raiox", "data"),
    Input("export_planilha_raiox", "n_clicks"),
    State("tabela_lab_raiox", "data")
)
def exportar_planilha(n, dados):
    if n is not None:
        df_export = pd.DataFrame(dados)

        return dcc.send_data_frame(df_export.to_excel, "dados.xlsx", sheet_name="LABORATORIO_RAIOX")
    
@app.callback(
    Output("modal_add_coluna_raiox", "is_open"),
    Output("nome_coluna_add_coluna_raiox", "value"),
    Output("tipo_coluna_add_coluna_raiox", "value"),
    Input("add_coluna_lab_raiox", "n_clicks"),
    Input("fechar_modal_add_coluna_raiox", "n_clicks"),
    Input("botao_add_coluna_raiox", "n_clicks"),
    State("modal_add_coluna_raiox", "is_open"),
    State("nome_coluna_add_coluna_raiox", "value"),
    State("tipo_coluna_add_coluna_raiox", "value")
)
def controlar_modal(btn_abrir, btn_fechar, btn_atualizar, is_open, nome_coluna, tipo_coluna):
    if btn_atualizar:
        if (nome_coluna and tipo_coluna) is not None:
            match tipo_coluna:
                case "Data":
                    tipo = "DATE"
                case "Texto":
                    tipo = "VARCHAR(MAX)"
                case "Número":
                    tipo = "REAL"
            
            ins = f"ALTER TABLE PCP_PLANTA.dbo.LABORATORIO_RAIOX ADD [{nome_coluna}] {tipo};"

            with engine.connect() as conn:
                try:
                    conn.execute(text(ins))
                except Exception as e:
                    print(f"Algo deu errado: {e}")
                finally:
                    conn.close()
        return [not is_open, "", ""]
    
    elif (btn_abrir or btn_fechar):
        return [not is_open, "", ""]
    
    else:
        return [is_open, "", ""]
    
@app.callback(
    Output("modal_remove_coluna_raiox", "is_open"),
    Input("remove_coluna_raiox", "n_clicks"), 
    Input("fechar_modal_remove_coluna_raiox", "n_clicks"),
    Input("botao_remove_coluna_raiox", "n_clicks"),
    State("modal_remove_coluna_raiox", "is_open")
)
def controlar_modal_remover_coluna(abrir, fechar, confirmar, is_open):
    if confirmar:
        return not is_open
    elif (abrir or fechar):
        return not is_open
    else:
        return is_open

# @app.callback(
#     Output("dropdown_colunas_lab_raiox", "options"),
#     Input("add_coluna_lab_raiox", "n_clicks"),
#     Input("remove_coluna_raiox", "n_clicks")
# )
# def popular_dropdown_colunas(n_add, n_remove):
#     if (n_add or n_remove):
#         df_drop = pd.DataFrame(pd.read_sql("SELECT * FROM LABORATORIO_RAIOX", conn))

#         arr = [ col for col in df_drop.columns ]

#         return arr
        