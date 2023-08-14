from dash import dash, html, dash_table, dcc, Input, Output, State
from app import *
from connection_lab import *
from pages import navbar
from datetime import datetime
from dash.exceptions import PreventUpdate
from sqlalchemy import text
from flask_login import current_user
from functools import wraps
from numpy import nan
from datetime import date

import dash_bootstrap_components as dbc
import pandas as pd
import io
import base64
import re

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != 'lab_pcp':
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

df = pd.DataFrame(pd.read_sql("SELECT * FROM LABORATORIO2", conn))
df_data = df.loc[:, ["DATA"]]
# menor_data = datetime.strptime(str(df_data["DATA"].min()), "%Y/%m/%d %H:%M:%S.%f")
# print(menor_data)
# menor_dia, menor_mes, menor_ano = menor_data.day, menor_data.month, menor_data.year
# maior_data = datetime.strptime(str(df_data["DATA"].max()), "%Y/%m/%d %H:%M:%S.%f")
# maior_dia, maior_mes, maior_ano = maior_data.day, maior_data.month, maior_data.year
menor_data = df_data["DATA"].min()
menor_ano, menor_mes, menor_dia = int(str(menor_data)[0:4]), int(str(menor_data)[5:7]), int(str(menor_data)[8:10])
menor_data = menor_data.strftime("%Y-%m-%d")

maior_data = df_data["DATA"].max()
maior_ano, maior_mes, maior_dia = int(str(maior_data)[0:4]), int(str(maior_data)[5:7]), int(str(maior_data)[8:10])
maior_data = maior_data.strftime("%Y-%m-%d")

hoje = date.today()

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

    dcc.Location(id="base_url_mpaes", refresh=True),

    dbc.Row([
        dbc.Card([
            html.Legend("Filtro por data"),
            dcc.DatePickerSingle(id="datepicker_lab", display_format="DD/MM/YYYY", month_format="DD/MM/YYYY", min_date_allowed=menor_data, max_date_allowed=hoje, date=hoje, style={"margin-bottom": "5px"}),
            dcc.Dropdown(id="dropdown_colunas_lab", options=[i for i in df.columns], multi=True, placeholder="Colunas", value=["DATA", "CODIGO"]),
            
        ], style={"width": "45%","height": "100%",'padding': '25px','align-self': 'center','display': 'flex','flex-direction': 'column', "justify-content": "center", 'margin-right': '5%'}),

        dbc.Card([
            html.Legend("Funções"),
            dbc.Row([
                dbc.Button("Declarar não recebimento", id="decl_mpaes", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Adicionar coluna", id="add_coluna_mpaes", style={"margin": "2px", "width": "40%"}),
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),
            dbc.Row([
                dbc.Button("Importar dados", id="import_lab_mpaes", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Excluir registro", id="exc_registro_mpaes", style={"margin": "2px", "width": "40%"})
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),
            dbc.Row([
                dbc.Button("Exportar dados", id="export_planilha_mpaes", style={"margin": "2px", "width": "40%"}),
                dbc.Button("Remover coluna", id="remove_coluna_mpaes", style={"margin": "2px", "width": "40%"})
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"}),
            dbc.Row([
                dcc.Checklist([" Editável"], id="editable_check", inline=True),
                dcc.Checklist([" Selecionável"], id="selectable_check", inline=True)
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"})
            
        ], style={"width": "45%","height": "100%",'padding': '25px','align-self': 'center','display': 'flex','flex-direction': 'column', 'margin-left': '5%'})
    ], style={"height": "40%", "width": "80%", "margin": "10px", "display": "flex", "flex-direction": "row", "justify-content": "center"}),

    dbc.Row([
        dbc.Card([
            html.Legend("Dados"),
            dash_table.DataTable(id="tabela_lab", data=[{}], style_table={"height": '300px', 'overflowY': 'auto'}, editable=False, style_cell={"textAlign": "left"}, style_header={"fontWeight": "bold"}, style_as_list_view=False)
        ],style=card_style)
    ], style={"height": "55%", "width": "80%", "margin": "10px"}),

], style={"display": 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'})



def render_layout(user):
    username = user.nm_usr

    layout = html.Div([
        dcc.Location(id="lab_mpaes_url", refresh=True),
        dcc.Download(id="download"),

        # <==========> Modais <==========>

        dbc.Modal([

            dbc.ModalHeader(dbc.ModalTitle("Criar nova coluna")),

            dbc.ModalBody([

                dbc.Input(id="nome_coluna_add_coluna_mpaes", placeholder="Nome da nova coluna", style={"margin-bottom": "5px"}),

                dcc.Dropdown(id="tipo_coluna_add_coluna_mpaes", options=["Data", "Texto", "Número"], placeholder="Tipo de dado")

            ]),

            dbc.ModalFooter([

                dbc.Button("Fechar", id="fechar_modal_add_coluna_mpaes", class_name="ms-auto"),

                dbc.Button("Adicionar", id="botao_add_coluna_mpaes", class_name="ms-auto")
            ])

        ], id="modal_add_coluna_mpaes", is_open=False),

        dbc.Modal([

            dbc.ModalHeader(dbc.ModalTitle("Remover colunas")),

            dbc.ModalBody([
                dcc.Dropdown(id="coluna_remover_mpaes", options=[ col for col in df.columns ], multi=True, placeholder="Colunas")
            ]),

            dbc.ModalFooter([

                dbc.Button("Fechar", id="fechar_modal_remove_coluna_mpaes", class_name="ms-auto"),

                dbc.Button("Remover", id="botao_remove_coluna_mpaes", class_name="ms-auto")

            ])

        ], id="modal_remove_coluna_mpaes", is_open=False),

        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Importar dados")),

            dbc.ModalBody([

                dcc.Upload(id="upload_mpaes", children=[
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

            

            dash_table.DataTable(id="tabela_importar_mpaes", data=[{}])
            ], id="modal_import_body_mpaes"),

            dbc.ModalFooter([
                dcc.Dropdown(id="hora_import", options=["02", "05", "08", "11", "14", "17", "20", "23"], placeholder="Hora da amostra"),
                dbc.Button("Importar", id="botao_confirmar_import_dados_mpaes", class_name="ms-auto")
            ])

        ], id="modal_import_mpaes", is_open=False, size="l"),

        dbc.Modal([

            dbc.ModalHeader(dbc.ModalTitle("Declarar não recebimento")),

            dbc.ModalBody([

                html.Div([
                    dcc.DatePickerSingle(id="data_n_receb", date=date.today(), month_format="DD/MM/YYYY", display_format="DD/MM/YYYY", style={"margin-bottom": "10px"}),

                    dcc.Dropdown(id="hr_n_receb", options=[
                        "02:00", "05:00", "08:00", "11:00", "14:00", "17:00", "20:00", "23:00"
                    ])
                ], className="container align-self-center")
                
            ]),

            dbc.ModalFooter([
                dbc.Button("Declarar", id="decl_n_receb", class_name="ms-auto")
            ])

        ], id="modal_decl_n_receb", is_open=False, size="l"),

        html.H1("", id="gateway_import_mpaes", hidden="hidden"),
        html.H1("", id="gateway_delete_mpaes", hidden="hidden"),

        navbar.nav()[0],
            dbc.Row([   
                content
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return layout



# <==========> Callbacks <==========> 

@app.callback(
    Output("tabela_lab", "data"),
    Output("tabela_lab", "columns"),
    Input("datepicker_lab", "date"),
    Input("dropdown_colunas_lab", "value")
)
def preencher_tabela(data, colunas):
    ano = data[0:4]
    mes = data[5:7]
    dia = data[8:10]
    df_filtrado = pd.DataFrame(pd.read_sql(f"SELECT * FROM LABORATORIO2 WHERE CAST(DATA AS DATE) = '{data}'", conn))

    if len(colunas) != 0:
        df_filtrado = df_filtrado.loc[:, [ str(col) for col in colunas ]]
    # print(df_filtrado)
    values = df_filtrado.to_dict(orient="records")
    cols = [ {"name": str(col), "id": str(col)} for col in df_filtrado.columns ]

    return [ values, cols ]

@app.callback(
    Output("tabela_lab", "row_selectable"),
    Input("selectable_check", "value"),
)
def ativar_selectable(value):
    if(current_user.usr_role == "lab_pcp"):
        return None if((value is None) or (len(value)==0)) else "single"
    else:
        return None

@app.callback(
    Output("tabela_lab", "editable"),
    Input("editable_check", "value")
)
def ativar_editable(value):
    return False if((value is None) or (len(value)==0)) else True

@app.callback(
    Output("download", "data"),
    Input("export_planilha_mpaes", "n_clicks"),
    # State("datepicker_lab", "date"),
    State("tabela_lab", "data"),
    # State("dropdown_colunas_lab", "value"),
)
def exportar_planilha(n, dados):
    if n is None:
        raise PreventUpdate
    else:
        df_export = pd.DataFrame(dados)

        return dcc.send_data_frame(df_export.to_excel, "dados.xlsx", sheet_name="LABORATORIO_MPAES")
    
@app.callback(
    Output("modal_add_coluna_mpaes", "is_open"),
    Output("nome_coluna_add_coluna_mpaes", "value"),
    Input("add_coluna_mpaes", "n_clicks"),
    Input("fechar_modal_add_coluna_mpaes", "n_clicks"),
    Input("botao_add_coluna_mpaes", "n_clicks"),
    State("modal_add_coluna_mpaes", "is_open"),
    State("nome_coluna_add_coluna_mpaes", "value"),
    State("tipo_coluna_add_coluna_mpaes", "value")
)
def controlar_modal_add_coluna(btn_abrir, btn_fechar, btn_atualizar, is_open, nome_coluna, tipo_coluna):
    if btn_atualizar:
        if (nome_coluna and tipo_coluna) is not None:
            match tipo_coluna:
                case "Data":
                    tipo = "DATE"
                case "Texto":
                    tipo = "VARCHAR(MAX)"
                case "Número":
                    tipo = "REAL"
            ins = f"ALTER TABLE PCP_PLANTA.dbo.LABORATORIO2 ADD [{nome_coluna}] {tipo};"
            print(ins)

            if(current_user.usr_role == "lab_pcp"):
                with engine.connect() as conn:
                    try:
                        conn.execute(text(ins))
                        print('certo')
                    except Exception as e:
                        print(f"Algo deu errado: {e}")
                        print("Erro")
                    finally:
                        conn.close()
        return [not is_open, ""]
    
    elif (btn_abrir or btn_fechar):
        return [not is_open, ""]
    else:
        return [is_open, ""]

@app.callback(
    Output("modal_remove_coluna_mpaes", "is_open"),
    Input("remove_coluna_mpaes", "n_clicks"), 
    Input("fechar_modal_remove_coluna_mpaes", "n_clicks"),
    Input("botao_remove_coluna_mpaes", "n_clicks"),
    State("modal_remove_coluna_mpaes", "is_open"),
    State("coluna_remover_mpaes", "value")
)
def controlar_modal_remover_coluna(abrir, fechar, confirmar, is_open, coluna):
    if confirmar:
        if coluna is not None:
            for col in coluna:
                ins = f"ALTER TABLE LABORATORIO2 DROP COLUMN [{col}];"

                if(current_user.usr_role == "lab_pcp"):
                    with engine.connect() as conn:
                        try:
                            conn.execute(text(ins))
                            print(ins)
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
    Output("modal_import_mpaes", "is_open"),
    Output("modal_import_mpaes", "children"),
    Input("import_lab_mpaes", "n_clicks"),
    State("modal_import_mpaes", "is_open")
)
def controlar_modal_import(n, is_open):
    content = (
        dbc.ModalHeader(dbc.ModalTitle("Importar dados")),

            dbc.ModalBody([

                dcc.Upload(id="upload_mpaes", children=[
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

            

            dash_table.DataTable(id="tabela_importar_mpaes", data=[{}])
            ], id="modal_import_body_mpaes"),

            dbc.ModalFooter([
                dcc.Dropdown(id="hora_import", options=["02", "05", "08", "11", "14", "17", "20", "23"], placeholder="Hora da amostra", style={"width": "60%"}),
                dbc.Button("Importar", id="botao_confirmar_import_dados_mpaes", class_name="ms-auto")
            ])
    )

    if n:
        return [not is_open, content]
    return [is_open, content]

@app.callback(
    Output("dropdown_colunas_lab", "options"),
    Output("coluna_remover_mpaes", "options"),
    Input("modal_add_coluna_mpaes", "is_open"),
    Input("modal_remove_coluna_mpaes", "is_open")
)
def atualizar_colunas_tempo_real(is_open_add, is_open_remove):
    if((is_open_add) or (not is_open_add) or (is_open_remove) or (not is_open_remove)):
        df_colunas = pd.DataFrame(pd.read_sql("select * from LABORATORIO2", conn))
        arr = [ col for col in df_colunas.columns ]

        return [arr, arr] 
    
def parse_contents(contents, filename, hora):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), index_col=False
                )
        elif 'xlsx' in filename or 'xls' in filename:
            df = pd.read_excel(
                io.BytesIO(decoded), index_col=0
            )
        
        colunas_banc = [ col for col in pd.read_sql('SELECT * FROM LABORATORIO2', conn).columns ]
        colunas = df.iloc[11][1:]
        colunas_s_nan = [ ]
        for col in list(colunas.values):
            if str(col) != "nan":
                colunas_s_nan.append(col)

        colunas_upper = list(map(lambda x: x.upper(), colunas_s_nan))
        colunas_faltantes = list(filter(lambda x: x not in colunas_banc, colunas_upper))
        
        df_altura = df.shape[0]
        codigo_amostra = df.columns[1]
        data = df.iloc[3][1]
        tipo_analises = [ df.iloc[i][0] for i in range(14, df_altura)]
        # for i in range(14, df_altura):
            # tipo_analises.append(df.iloc[i][0])

        if colunas_faltantes == None or len(colunas_faltantes) == 0:
            df = df.iloc[13:][1:]
            # analises = list(df.iloc[0:][list(df.iloc[0:])[0]])
            df.insert(0, "TIPO_ANALISE", tipo_analises)
            if hora == None:
                df.insert(1, "DATA", [ data for i in range(df_altura-14) ])
            else:
                df.insert(1, "DATA", [ f"{data} {hora}:00:00" for i in range(df_altura-14) ])
            df.insert(2, "CODIGO_AMOSTRA", [ codigo_amostra for i in range(df_altura-14) ])
            df.pop("COA:")
            colunas_df = df.columns
            for i in range(0, len(colunas_upper)):
                df.rename(columns={f"{colunas_df[i+3]}": f"{colunas_upper[i]}"}, inplace=True)
            df = df.dropna(axis=1)

            # df.insert(0,"CODIGO_AMOSTRA", [codigo_amostra for i in range(df_altura-14)])
            
            return html.Div([
                dash_table.DataTable(
            df.to_dict(orient="records"),
            [{'name': i, 'id': i} for i in df.columns], style_table={"height": "300px", "overflowY": "auto"}, editable=False, style_cell={"textAlign": "left"}, style_header={"fontWeight": "bold"}, style_as_list_view=False, 
            id="tabela_importar_mpaes"
        ),

        html.Hr(),  # horizontal line

       
        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])

        if colunas_faltantes != None:
            return html.Div([
                f"""Uma ou mais colunas existentes no arquivo não existem no banco de dados. 
                Por favor, adicione-as manualmente.
                [{colunas_faltantes}]"""
            ])


        # print(codigo_amostra)
        # print(data)
        # print(list(colunas.values))
        # print(colunas_s_nan)
        # print(tipo_analises)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns], style_table={"height": "300px", "overflowY": "auto"}, editable=False, style_cell={"textAlign": "left"}, style_header={"fontWeight": "bold"}, style_as_list_view=False, 
            id="tabela_importar_mpaes"
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
    Output("modal_import_body_mpaes", "children"),
    Input('upload_mpaes', 'contents'),
    State('upload_mpaes', 'filename'),
    State('hora_import', 'value')
)
def update_output(list_of_contents, list_of_names, hora):
    if list_of_contents is None:
        return (dcc.Upload(id="upload_mpaes", children=[
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
            
            # dcc.Dropdown(id="hora_import", options=["02", "05", "08", "11", "14", "17", "20", "23"], placeholder="Hora da amostra"),
            dash_table.DataTable(id="tabela_importar_mpaes", data=[{}])
            )
    
    if list_of_contents is not None:
        children = []
        # for c,n,d in zip(list_of_contents, list_of_names, list_of_dates):
        #     print(c,n, d) 
        children = [
            parse_contents(list_of_contents, list_of_names, hora)]
        return children


# def dataframe_to_sql_insert_new_func(df):

#     data = [ tuple(row) for row in df.values ]
#     colunas = [ f"[{col}]" for col in df.columns ]

#     inserts = [ ]
#     for d in data:
#         inserts.append(f"INSERT INTO LABORATORIO2 ({', '.join(colunas)}) VALUES {d}")
#     sql_insert = f"INSERT INTO LABORATORIO2 ({', '.join(colunas)}) VALUES ({data[0]})"

#     return inserts

import pandas as pd

def dataframe_to_sql_insert_new_func(df):
    data = [tuple(row) for row in df.values]
    colunas = [f"[{col}]" for col in df.columns]

    inserts = []
    pattern = r"\b\d{2}/\d{2}/\d{4}\b"
    for d in data:
        values = []
        for value in d:
            if value == d[1]:
                ins = f"CONVERT(DATETIME, '{value}', 103)"
            else:
                ins = f"'{value}'"
            values.append(ins)
        inserts.append(f"INSERT INTO LABORATORIO2 ({', '.join(colunas)}) VALUES ({', '.join(values)})")

    return inserts


@app.callback(
    Output("gateway_import_mpaes", "children"),
    Input("botao_confirmar_import_dados_mpaes", "n_clicks"),
    State("tabela_importar_mpaes", "data"),
    prevent_initial_call=True
)
def botao_importar_modal(n, dados):
    if n is None:
        raise PreventUpdate
    
    if n:
        df = DataFrame(dados)
        # sql_insert = dataframe_to_sql_insert(df, tableName)
        sql_insert = dataframe_to_sql_insert_new_func(df)
        pattern = r"\b\d{2}/\d{2}/\d{4}\b"

        for ins in sql_insert:
            data = re.findall(pattern, ins)

            # print(ins)
            with engine.connect() as conn:
                    try:
                        # ins.replace(data[0], f"CONVERT(DATETIME, '{data}', 103)")
                        # print(ins)
                        conn.execute(text(ins.replace("None", "NULL")))
                    except Exception as e:
                        print(f"Algo deu errado: {e}")
                    finally:
                        conn.close()
        return ""

# @app.callback(
    
# )
# def excluir_registro()
@app.callback(
    Output("tabela_importar_mpaes", "data"),
    Input("hora_import", "value"),
    State("tabela_importar_mpaes", "data"),
    # State('upload_mpaes', 'contents')
)
def insert_hora_pos_upload(value, data):
    if value is None:
        raise PreventUpdate
    if value:
        df = pd.DataFrame(data)
        if df.empty:
            raise PreventUpdate
        else:
            v = df["DATA"].iloc[0]
            if len(v) == 10:
                df["DATA"] = df["DATA"].map({f"{v}": f"{v} {value}:00:00"})
            else:
                pass

            return df.to_dict(orient="records")
        
@app.callback(
    Output("modal_decl_n_receb", "is_open"),
    Input("decl_n_receb", "n_clicks"),
    Input("decl_mpaes", "n_clicks"),
    State("modal_decl_n_receb", "is_open"),
    State("data_n_receb", "date"),
    State("hr_n_receb", "value")
)
def controlar_modal_decl_n_receb(confirm, n, is_open, date, hour):
    if n:
        if not confirm:
            return not is_open
        else:
            if date and hour:
                try:
                    with engine.connect() as conn:
                        ins = f"INSERT INTO LABORATORIO2(DATA, TIPO_ANALISE, CODIGO_AMOSTRA) VALUES (CONVERT(DATETIME, '{date} {hour}:00.000', 103), 'NÃO RECEBIDA', 'NÃO RECEBIDA')"
                        conn.execute(text(ins))
                    
                        return not is_open
                except Exception as e:
                    print(f"{e}")

                    return is_open
    return is_open 