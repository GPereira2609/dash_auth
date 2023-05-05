from app import *
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import logout_user, current_user
from sqlalchemy import text
from functools import wraps

from globals import *

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != 'admin':
            return ''
        return func(*args, **kwargs)
    return decorated_view


card_style = {
    'width': '30vw',
    'min-height': '450px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}

card_style2= {
    'width': '90vw',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}


def render_layout(user):
    username = user.nm_usr

    df = DataFrame(read_sql("select * from tbl_Paradas", engine.connect()))
    
    layout = html.Div([
            dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Col([
                            html.Img(src=app.get_asset_url('do-utilizador.png'), height=70, width=70), 
                        ], style={"display": "flex", "flex-direction": "column", "justify-content": "center"}),
                        dcc.Location(id="consultar_paradas_base_url"),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col()
                ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'height': "100%", "margin-left": "10 auto", "align-items": "left"}),

  

                    html.Div([
                        dbc.Nav([
                            dbc.NavLink("Home", href="/home", active="exact"),

                            dbc.DropdownMenu([
                                dbc.NavLink("Consultar paradas", href="/consultar_paradas", active="exact"),
                                dbc.NavLink("Apropriar paradas", href="/aprop_paradas", active="exact"),
                            ], label="Paradas", nav=True),

                            dbc.DropdownMenu([
                                dbc.NavLink("Consultar turno", href="/consultar_turno", active="exact"),
                                dbc.NavLink("Apropriação turno", href="/aprop_turno", active="exact"),
                            ], label="Turno", nav=True),

                            dbc.DropdownMenu([
                                dbc.NavLink("Registrar usuário", href="/register", active="exact"),
                                dbc.NavLink("Sair", href="/logout")
                            ], label="Usuário", nav=True),
                        ], pills=True, vertical=False, id='nav')
                    ], style={"height": "100%", 'display': 'flex', 'flex-direction': 'column'}),

                    html.Div([
                        html.Img(src=app.get_asset_url('f2711217-e0a9-4a63-a24c-3c969b7ce090.png'), height=70, width=194),
                    ], style={"margin-right": "0", "padding": "0"})
                ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-evenly'}),
            ], style={"display": "flex", "flex-direction": "column", "justify-content": "space-between"})
                
            ], style={"height": '15%', 'width': '105vw', 'display': 'flex', "flex-direction": "row", 'justify-content': 'space-between', 'background-color': '#298753'}),

            dbc.Row([   
                html.Div([
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.Legend("Processo/equipamento"),
                                dbc.Row([
                                    dbc.Label("Processo: "),
                                    dcc.Dropdown(options=popular_dropdown_processo_consultar_paradas(), id="dropdown_processo_consultar_paradas")
                            ]),
                                dbc.Row([
                                    dbc.Label("Sistema: "),
                                    dcc.Dropdown(options=[], id="dropdown_sistema_consultar_paradas")
                            ]),
                                dbc.Row([
                                    dbc.Label("Equipamento: "),
                                    dcc.Dropdown(options=[], id="dropdown_equipamento_consultar_paradas")
                            ]),
                                dbc.Row([
                                    dbc.Label("Colunas: "),
                                    dcc.Dropdown([
                                        i for i in df.columns
                                       
                                    ],value=[
                                        "Id", "Validade", "Equipamento", "DataInicio", "DataFim", "Duracao", "EqpGerador", "GrupoCodigo", "Turno"
                                    ], id="checklist_campos_tabela", multi=True)
                                ])
                            ], style=card_style),
                            
                            ]),

                        dbc.Col([
                            dbc.Card([
                                html.Legend("Apropriação"),

                                dbc.Row([
                                    dbc.Label("Tipo de Código: "),
                                    dcc.Dropdown(id="dropdown_tipocodigo_consultar_paradas", options=popular_tipo_codigo_consultar_paradas())
                                ]),

                                dbc.Row([
                                    dbc.Label("Grupo de Código: "),
                                    dcc.Dropdown(id="dropdown_grupocodigo_consultar_paradas", options=[])
                                ]),

                                dbc.Row([
                                    dbc.Label("Código das Falhas: "),
                                    dcc.Dropdown(id="dropdown_codigofalha_consultar_paradas", options=[])
                                ]),

                                dbc.Row([
                                    dbc.Label("Causa Aparente: "),
                                    dcc.Dropdown(id="dropdown_causaaparente_consultar_paradas", options=[])
                                ]),

                                dbc.Row([
                                    dbc.Label("Componente: "),
                                    dcc.Dropdown(id="dropdown_componente_consultar_paradas", options=popular_componente_consultar_parada())
                                ])
                            ], style=card_style)
                        ]),

                        dbc.Col([
                            dbc.Card([
                                html.Legend("Período"),
                                dbc.Row([
                                    dbc.Label("Início: "),
                                    dcc.DatePickerSingle(display_format="DD/MM/YYYY", id="data_inicio_consultar_paradas", min_date_allowed=menor_data_inicio())
                            ]),

                                dbc.Row([
                                    dbc.Label("Fim: "),
                                    dcc.DatePickerSingle(display_format="DD/MM/YYYY", id="data_fim_consultar_paradas", min_date_allowed=menor_data_fim())
                            ]),

                                dbc.Row([
                                    dbc.Label("Turno: "),
                                    dcc.Dropdown(id="consultar_paradas_turno", options=popular_turnos())
                                ]),

                                dbc.Row([
                                    dbc.Button("Consultar", id="botao_consulta_paradas", style={"margin": "10px", 'width': '100px'})
                                ])
                            ], style=card_style),
                            
                        ])
                        ], style={"padding-top": "25px"}),

                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    html.Legend("Dados"),
                                    dbc.Row([
                                        dash_table.DataTable(id="tabela_dados", data=[{}], selected_rows=[], page_action='none', style_table={"height": '300px', 'overflowY': 'auto'})
                                    ])
                                ], style=card_style2)
                            ])
                        ], style={"padding-top": "25px"}),

                        dbc.Row([
                            dbc.Col([
                                html.H4("ID selecionado: ", id="marcador_id_consultar_paradas"),
                                dbc.Button("Atualizar", id="atualizar_consultar_paradas", style={"margin": "10px", 'width': '100px'}),
                                dbc.Button("Excluir", id="excluir_consultar_paradas", style={"margin": "10px", 'width': '100px'}),
                                html.H4(id="gateway_instrucoes"),
                                dbc.Button("Dividir", id="dividir_consultar_paradas", style={"margin": "10px", 'width': '100px'}),
                                dbc.Modal([
                                    dbc.ModalHeader(dbc.ModalTitle("Dividir")),
                                    dbc.ModalBody([
                                        html.Div([
                                            dbc.Label("Escolha a hora da divisão: "),
                                            dbc.Input(id="input_modal_dividir", type="time"),
                                            html.H4(id="msg_modal_dividir")
                                        ], style={"display": "flex", "flex-direction": "column", "justify-content": "center"})
                                    ]),
                                    dbc.ModalFooter([
                                        dbc.Button("Fechar", id="fechar_modal_dividir"),
                                        dbc.Button("Atualizar", id="atualizar_modal_dividir")
                                    ])
                                ], id="modal_dividir_consultar_paradas"),
                                dbc.Button("Copiar", id="copiar_consultar_paradas", style={"margin": "10px", 'width': '100px'}),
                                html.H4(id="gateway_instrucoes2")
                            ])
                        ])
                        

                    ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin-left": "10px"})


            ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
        ], style={'background-color': "white", 'height': '100vh', 'width': '100vw', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'width': '100vw'})
        
    return layout

@app.callback(
    Output("dropdown_sistema_consultar_paradas", "options"),
    Input("dropdown_processo_consultar_paradas", "value")
)
def popular_dropdown_sistemas(value):
    if value is None:
        raise PreventUpdate
    if value is not None:
        return popular_dropdown_sistema_consultar_paradas(value)

@app.callback(
    Output("dropdown_equipamento_consultar_paradas", "options"),
    Input("dropdown_processo_consultar_paradas", "value"),
    Input("dropdown_sistema_consultar_paradas", "value")
)
def popular_dropdown_equipamento(value_processo, value_sistema):
    if value_processo is None:
        raise PreventUpdate
    if value_sistema is None:
        raise PreventUpdate
    return popular_dropdown_equipamento_consultar_paradas(value_processo, value_sistema) 

@app.callback(
    Output("tabela_dados", "row_selectable"),
    Input("botao_consulta_paradas", "n_clicks")
)
def controlar_row_selectable(n):
    if n is None:
        raise PreventUpdate
    if n is not None:
        return "single"

@app.callback(
    Output("tabela_dados", "data"),
    Output("tabela_dados", "columns"),
    Input("tabela_dados", "row_selectable"),
    [
        State("dropdown_sistema_consultar_paradas", "value"),
        State("dropdown_processo_consultar_paradas", "value"),
        State("dropdown_equipamento_consultar_paradas", "value"),
        State("data_inicio_consultar_paradas", "date"),
        State("data_fim_consultar_paradas", "date"),
        State("consultar_paradas_turno", "value"),
        State("dropdown_tipocodigo_consultar_paradas", "value"),
        State("dropdown_grupocodigo_consultar_paradas", "value"),
        State("dropdown_codigofalha_consultar_paradas", "value"),
        State("dropdown_causaaparente_consultar_paradas", "value"),
        State("dropdown_componente_consultar_paradas", "value"),
        State("checklist_campos_tabela", "value")
    ]
)
def consultar_paradas(n, sist, proc, equip, dt_inicio, dt_fim, turno, tipo_codigo, grupo_codigo, codigo_falha, causa_aparente, componente, colunas):
    flag = 0

    temp = ""
    if len(colunas) == 0:
        temp = "* "
    else:
        for coluna in colunas:
            temp += f"{coluna},"

    if (sist or proc or equip or dt_inicio or dt_fim or turno or tipo_codigo or grupo_codigo or codigo_falha or causa_aparente or componente) is None:
        raise PreventUpdate 
    if n != "single":
        raise PreventUpdate
    if n == 'single':

        ins = f"select {temp[:-1]} from tbl_Paradas where"
        if proc:
            flag = 1
            ins += f" Producao = '{proc}'"
        if sist:
            if flag == 1:
                ins += " and "
            flag = 1
            ins += f" Sistema = '{sist}'"
        if equip:
            if flag == 1:
                ins += ' and '
            flag = 1
            ins += f" Equipamento = '{equip}'"
        if dt_inicio and dt_fim:
            if flag == 1:
                ins += ' and '
            flag = 1
            ins += f" DataInicio >= '{dt_inicio}' and DataFim <= '{dt_fim} 23:59:59'"
        if turno:
            if flag == 1:
                ins += ' and ' 
            flag = 1
            ins += f" Turno = '{turno}'"
        if tipo_codigo:
            if flag == 1:
                ins += ' and '
            flag = 1
            ins += f" TipoCodigo = '{tipo_codigo}'"
        if grupo_codigo:
            if flag == 1:
                ins += ' and '
            flag = 1
            ins += f" GrupoCodigo = '{grupo_codigo}'"
        if codigo_falha:
            if flag == 1:
                ins += ' and '
            flag = 1
            ins += f" CodigoFalha = '{codigo_falha}'"
    
        if componente:
            if flag == 1:
                ins += ' and '
            flag = 1
            ins += f" Componente = '{componente}'"
        flag = 0
        
        df = DataFrame(read_sql(ins, conn))
        cols = []
        for col in df.columns:
            cols.append({"name": str(col), "id": str(col)})

        values = df.to_dict(orient="records")

        return [values, cols]

# @app.callback(
#     Output("tabela_dados", "data"),
#     Output("tabela_dados", "columns"),
#     Input("botao_consulta_paradas", "n_clicks"),
#     [
#         State("dropdown_sistema_consultar_paradas", "value"),
#         State("dropdown_processo_consultar_paradas", "value"),
#         State("dropdown_equipamento_consultar_paradas", "value"),
#         State("data_inicio_consultar_paradas", "date"),
#         State("data_fim_consultar_paradas", "date")   
#     ]
# )
# def consultar_paradas(n, sist, proc, equip, dt_inicio, dt_fim):
#     if (sist or proc or equip or dt_inicio or dt_fim) is None:
#         raise PreventUpdate 
#     if n is None:
#         raise PreventUpdate
#     if n is not None:
#         ins = f"select Id, Validade, Producao, Sistema, Equipamento, DataInicio, DataFim, Duracao, EqpGerador from tbl_Paradas where"
#         if sist:
#             ins += f" Sistema = '{sist}' and"
#         if proc:
#             ins += f" Producao = '{proc}' and"
#         if equip:
#             ins += f" Equipamento = '{equip}' and "
#         ins += f" DataInicio >= convert(Datetime, '{dt_inicio}') and DataFim <= convert(Datetime, '{dt_fim}')"
#         df = DataFrame(read_sql(ins, conn))
#         cols = []
#         for col in df.columns:
#             cols.append({"name": str(col), "id": str(col)})

#         values = df.to_dict(orient="records")

#         return [values, cols]

@app.callback(
    Output("marcador_id_consultar_paradas", "children"),
    Input("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
def mostrar_id_consultar_paradas(rows, tabela):
    if len(rows) != 0:
        data = str(tabela[rows[0]]["Id"])
        return f"ID selecionado: {data}"

@app.callback(
    Output("gateway_instrucoes", "children"),
    Input("excluir_consultar_paradas", "n_clicks"),
    State("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
@admin_required
def excluir_consultar_paradas(n, rows, tabela):
    if n is None:
        raise PreventUpdate
    if n is not None:
        if len(rows) != 0:
            id = str(tabela[rows[0]]["Id"])
            ins = f"delete from tbl_Paradas where Id = {int(id)}"
            with engine.connect() as conn:
                    conn.execute(text(ins))
                    conn.commit()
                    conn.close()
            return ''

@app.callback(
    Output("gateway_instrucoes2", "children"),
    Input("copiar_consultar_paradas", "n_clicks"),
    State("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
def copiar_consultar_paradas(n, rows, tabela):
    if n is None:
        raise PreventUpdate
    if n is not None:
        if len(rows) != 0:

            id = str(tabela[rows[0]]["Id"])

            ins = f"insert into tbl_Paradas(Validade, Producao, Sistema, Equipamento, DataInicio, DataFim, EqpGerador, TipoCodigo, GrupoCodigo, CodigoFalha, Turno, CausaAparente, Operador, Observacao, Componente, ModoFalha, Apropriador) select Validade, Producao, Sistema, Equipamento, DataInicio, DataFim, EqpGerador, TipoCodigo, GrupoCodigo, CodigoFalha, Turno, CausaAparente, Operador, Observacao, Componente, ModoFalha, Apropriador from tbl_Paradas where ID = {id}"
            

            with engine.connect() as conn:
                conn.execute(text(ins))
                conn.commit()
                conn.close()
            return ''
      


@app.callback(
    Output("input_modal_atualizar", "value"),
    Input("dropdown_modal_atualizar", "value"),
    State("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
def mostrar_input_id_atual(value, rows, tabela):
    if value is not None:
        id = tabela[rows[0]]["Id"]
        ins = f"select {value} from tbl_Paradas where Id = {int(id)}"
        df = DataFrame(read_sql(ins, conn))
        
        return df.values[0][0]

@app.callback(
    Output("modal_dividir_consultar_paradas", "is_open"),
    [
        Input("dividir_consultar_paradas", "n_clicks"),
        Input("fechar_modal_dividir", "n_clicks")
    ],
    State("modal_dividir_consultar_paradas", "is_open")
)
def controlar_modal_dividir(n_abrir, n_fechar, is_open):
    if n_abrir or n_fechar:
        return not is_open
    return is_open

# @app.callback(
#     Output("input_modal_dividir", "value"),
#     Input("input_modal_dividir", "value")
# )
# def validar_input_dividir(value):
#     if value is None:
#         raise PreventUpdate
    
#     if value is not None:
#         if len(value) == 3 and ":" in value:
#             return f"{value[:2]}"
#         elif len(value) == 3:
#             p1 = value[:2]
#             p2 = value[2:]
#             return f"{p1}:{p2}"
#         elif len(value) >= 5:
#             return f"{value[:5]}"
#         else:
#             return value

@app.callback(
    Output("msg_modal_dividir", "children"),
    Input("atualizar_modal_dividir", "n_clicks"),
    [
        State("input_modal_dividir", "value"),
        State("tabela_dados", "selected_rows"),
        State("tabela_dados", "data")
    ]
)
def dividir_parada(n, value, row, tabela):
    if n is None:
        raise PreventUpdate
    else:
        id = tabela[row[0]]["Id"]
        return [dividir_parada_func(nova_hora=value, id=id)]
        
@app.callback(
    Output("consultar_paradas_base_url", "pathname"),
    Input("atualizar_consultar_paradas", "n_clicks"),
    Input("tabela_dados", "selected_rows"),
    Input("tabela_dados", "data")
)
def atualizar_por_id(n, rows, tabela):
    if n is None:
        raise PreventUpdate
    else:
        if len(rows) != 0:
            id = tabela[rows[0]]["Id"]
            return f'/atualizar_parada/{id}'

@app.callback(
    Output("dropdown_grupocodigo_consultar_paradas", "options"),
    Input("dropdown_tipocodigo_consultar_paradas", "value")
)
def popular_tipo_codigo_filtrado(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select [Grupo de Código] from tbl_GrupoDeCódigo where [Tipo de Código] = '{value}'"
        df = DataFrame(read_sql(ins, engine.connect()))
        arr = []
        for i in df.drop_duplicates().values.tolist():
            if i[0] != 'Null':
                arr.append(i[0])

        return arr

@app.callback(
    Output("dropdown_codigofalha_consultar_paradas", "options"),
    Input("dropdown_grupocodigo_consultar_paradas", "value")
)
def popular_grupo_codigo_filtrado(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select [Código das Falhas] from tbl_CódigoDasFalhas where [Grupo de Código] = '{value}'"
        df = DataFrame(read_sql(ins, engine.connect()))
        arr = []
        for i in df.drop_duplicates().values.tolist():
            if i[0] != 'Null':
                arr.append(i[0])

        return arr

@app.callback(
    Output("dropdown_causaaparente_consultar_paradas", "options"),
    Input("dropdown_codigofalha_consultar_paradas", "value")
)
def popular_causa_aparente_filtrado(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select CausaAparente from tbl_CausaAparente where CodigoFalha = '{value}'"
        df = DataFrame(read_sql(ins, engine.connect()))
        arr = []
        for i in df.drop_duplicates().values.tolist():
            if i[0] != 'Null':
                arr.append(i[0])

        return arr