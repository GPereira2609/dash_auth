from dash import dash, html, dash_table, dcc, Input, Output, State
from app import *
from connection_lab import *
from pages import navbar
from datetime import datetime
from sqlalchemy import text
from dash.exceptions import PreventUpdate
from flask_login import current_user
from functools import wraps

import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != "lab_pcp":
            return ''
        return func(*args, **kwargs)
    return decorated_view

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

def dataframe_to_sql_insert(df, table_name):
    columns = ', '.join(df.columns)
    values = ', '.join(['%s'] * len(df.columns))

    # Cria uma lista de tuplas contendo os valores de cada linha do DataFrame
    data = [tuple(row) for row in df.values]

    inserts = []
    # Cria a instrução de inserção SQL
    for d in data:
        inserts.append(f"INSERT INTO {table_name} ({columns}) VALUES {d};")
    sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({data[0]});"

    return inserts

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

                dbc.Button("Importar dados", id="import_lab_raiox", style={"margin": "2px", "width": "40%"}),
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
                dcc.Dropdown(id="coluna_remover_raiox", options=[ col for col in df.columns ], multi=True, placeholder="Colunas")
            ]),

            dbc.ModalFooter([

                dbc.Button("Fechar", id="fechar_modal_remove_coluna_raiox", class_name="ms-auto"),

                dbc.Button("Remover", id="botao_remove_coluna_raiox", class_name="ms-auto")

            ])

        ], id="modal_remove_coluna_raiox", is_open=False),

        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Importar dados")),

            dbc.ModalBody([
                dcc.Upload(id="upload_raiox", children=[
                    html.Div([
                        "Arraste e solte ou ", html.A("Selecione os arquivos")
                    ])
                ], multiple=True, style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'}),

            dash_table.DataTable(id="tabela_importar_raiox", data=[{}])

            ], id="modal_import_body_raiox"),

            

            dbc.ModalFooter([
                dbc.Button("Importar", id="botao_confirmar_import_dados_raiox", class_name="ms-auto")
            ])
        ], id="modal_import_raiox", is_open=False, size="l"),

        html.H1("", id="gateway_import_raiox", hidden="hidden"),
        html.H1("", id="gateway_delete_raiox", hidden="hidden"),

        # ================================

        navbar.nav()[0],
            dbc.Row([   
                content
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return layout

# <==========> Callbacks <==========>
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
    Input("selectable_check_raiox", "value"),
)
def ativar_selectable_raiox(value):
    if current_user.usr_role == "lab_pcp":
        return None if((value is None) or (len(value)==0)) else "single"
    else:
        return None

@app.callback(
    Output("tabela_lab_raiox", "editable"),
    Input("editable_check_raiox", "value")
)
def ativar_editable_raiox(value):
    if(current_user.usr_role == "lab_pcp"):
        return False if ((value is None) or (len(value)==0)) else True
    else:
        return None
    
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

            if current_user.usr_role == "lab_pcp":
                with engine.connect() as conn:
                    try:
                        conn.execute(text(ins))
                    except Exception as e:
                        print(f"Algo deu errado: {e}")
                    finally:
                        conn.close()
        return [not is_open, ""]
    
    elif (btn_abrir or btn_fechar):
        return [not is_open, ""]
    else:
        return [is_open, ""]
    

    
@app.callback(
    Output("modal_remove_coluna_raiox", "is_open"),
    Input("remove_coluna_raiox", "n_clicks"), 
    Input("fechar_modal_remove_coluna_raiox", "n_clicks"),
    Input("botao_remove_coluna_raiox", "n_clicks"),
    State("modal_remove_coluna_raiox", "is_open"),
    State("coluna_remover_raiox", "value")
)
def controlar_modal_remover_coluna(abrir, fechar, confirmar, is_open, coluna):
    if confirmar:
        if coluna is not None:
            for col in coluna:
                ins = f"ALTER TABLE LABORATORIO_RAIOX DROP COLUMN [{col}];"

                if current_user.usr_role == "lab_pcp":
                    with engine.connect() as conn:
                        try:
                            conn.execute(text(ins))
                        except Exception as e:
                            print(f"Algo deu errado: {e}")
                        finally:
                            conn.close()
        return not is_open
    elif (abrir or fechar):
        return not is_open
    else:
        return is_open
    
@app.callback(
    Output("modal_import_raiox", "is_open"),
    Output("modal_import_raiox", "children"),
    Input("import_lab_raiox", "n_clicks"),
    State("modal_import_raiox", "is_open")
)
def controlar_modal_import(n, is_open):
    content = (
        dbc.ModalHeader(dbc.ModalTitle("Importar dados")),

            dbc.ModalBody([
                dcc.Upload(id="upload_raiox", children=[
                    html.Div([
                        "Arraste e solte ou ", html.A("Selecione os arquivos")
                    ])
                ], multiple=True, style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'}),

            dash_table.DataTable(id="tabela_importar_raiox", data=[{}])

            ], id="modal_import_body_raiox"),

            

            

            dbc.ModalFooter([
                dbc.Button("Importar", id="botao_confirmar_import_dados_raiox", class_name="ms-auto")
            ])
    )
    if n:
        return [not is_open, content]
    return [is_open, content]

@app.callback(
    Output("dropdown_colunas_lab_raiox", "options"),
    Output("coluna_remover_raiox", "options"),
    Input("modal_add_coluna_raiox", "is_open"),
    Input("modal_remove_coluna_raiox", "is_open")
)
def atualizar_colunas_tempo_real(is_open_add, is_open_remove):
    if((is_open_add) or (not is_open_add) or (is_open_remove) or (not is_open_remove)):
        df_colunas = pd.DataFrame(pd.read_sql("select * from LABORATORIO_RAIOX", conn))
        arr = [ col for col in df_colunas.columns ]

        return [arr, arr] 
    
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), index_col=0
                )
        elif 'xlsx' in filename or 'xls' in filename:
            df = pd.read_excel(
                io.BytesIO(decoded), index_col=0
            )

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns], style_table={"height": "300px", "overflowY": "auto"}, editable=False, style_cell={"textAlign": "left"}, style_header={"fontWeight": "bold"}, style_as_list_view=False, 
            id="tabela_importar_raiox"
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])

@app.callback(
    Output("modal_import_body_raiox", "children"),
    Input('upload_raiox', 'contents'),
    State('upload_raiox', 'filename')
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is None:
        return (dcc.Upload(id="upload_raiox", children=[
                    html.Div([
                        "Arraste e solte ou ", html.A("Selecione os arquivos")
                    ])
                ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',      
            'textAlign': 'center',
            'margin': '10px'}),
            
            dash_table.DataTable(id="tabela_importar_raiox", data=[{}])
            )
    
    if list_of_contents is not None:
        children = []
        # for c,n,d in zip(list_of_contents, list_of_names, list_of_dates):
        #     print(c,n, d) 
        children = [
            parse_contents(list_of_contents, list_of_names)]
        return children
        
@app.callback(
    Output("gateway_import_raiox", "children"),
    Input("botao_confirmar_import_dados_raiox", "n_clicks"),
    State("tabela_importar_raiox", "data"),
    prevent_initial_call=True
)
def botao_importar_modal(n, data):
    if n is None:
        raise PreventUpdate
    
    if n is not None:
        df = DataFrame(data)

        tableName = "LABORATORIO_RAIOX"
        sql_insert = dataframe_to_sql_insert(df, tableName)

        for ins in sql_insert:
            with engine.connect() as conn:
                    try:
                        conn.execute(text(ins.replace("None", "NULL")))
                    except Exception as e:
                        print(f"Algo deu errado: {e}")
                    finally:
                        conn.close()
        return ""
    
@app.callback(
    Output("gateway_delete_raiox", "children"),
    Input("exc_registro_lab_raiox", "n_clicks"),
    State("selectable_check_raiox", "value"),
    State("tabela_lab_raiox", "selected_rows"),
    State("dropdown_colunas_lab_raiox", "value"),
    State("datepicker_lab_raiox", "date")
)
def excluir_registro(n, value, rows, colunas, date):
    if n is None:
        raise PreventUpdate

    if n:
        if value == None:
            pass
        else:
            if current_user.usr_role == "lab_pcp":
                with engine.connect() as conn:
                    df_exclusao = DataFrame(read_sql(f"SELECT * FROM LABORATORIO_RAIOX WHERE CAST(DATA AS DATE) = '{date}'", conn))

                    df = df_exclusao.iloc[rows[0]]

                    try:
                        id = df["CODIGO"]
                        conn.execute(text(f"DELETE FROM LABORATORIO_RAIOX WHERE CODIGO = {id}"))
                    except Exception as e:
                        print(f"Algo deu errado: {e}")
                    finally:
                        conn.close()
            
            # print(df["CODIGO"])
    
        return ""

@app.callback(
    Output("datepicker_lab_raiox", "min_date_allowed"),
    Output("datepicker_lab_raiox", "max_date_allowed"),
    Output("datepicker_lab_raiox", "date"),
    Input("add_registro_lab_raiox", "n_clicks"),
    Input("import_lab_raiox", "n_clicks"),
    Input("exc_registro_lab_raiox", "n_clicks")
)
def atualizar_datas(n_add, n_import, n_delete):
    if n_add is None:
        raise PreventUpdate
    if n_import is None:
        raise PreventUpdate
    if n_delete is None:
        raise PreventUpdate
    if(n_add or n_import or n_delete):
        ins = "select * from LABORATORIO_RAIOX"
        df = pd.DataFrame(pd.read_sql(ins, conn))
        df_data = df.loc[:, ["DATA"]]
        menor_data = datetime.strptime(str(df_data["DATA"].min()), "%Y-%m-%d %H:%M:%S")
        maior_data = datetime.strptime(str(df_data["DATA"].max()), "%Y-%m-%d %H:%M:%S")

        print(menor_data)
        print(maior_data)

        return [menor_data, maior_data, maior_data]
