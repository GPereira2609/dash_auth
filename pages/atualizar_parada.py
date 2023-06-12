import dash_bootstrap_components as dbc
from dash import dcc, html, Input,Output, State
from app import *
from flask_login import logout_user, current_user
from dash.exceptions import PreventUpdate
from pandas import DataFrame, read_sql
from connection import conn
from globals import *
from functools import wraps
from pages import navbar

import time

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != 'admin':
            return ''
        return func(*args, **kwargs)
    return decorated_view


card_style = {
    'margin-top': '25px',
    'width': '500px',
    'min-height': '550px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}

def render_layout(user, id):
    username = user.nm_usr
    df_atual = DataFrame(read_sql(f"select * from tbl_Paradas where id = {id}", conn))

    hora_inicio = str(df_atual["DataInicio"][0])[11:]
    hora_fim = str(df_atual["DataFim"][0])[11:]

    template = html.Div([
        dcc.Location(id="atualizar_paradas_base_url"),
        navbar.nav()[0],
        dbc.Row([   
            html.Div([
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.Legend("Operação"),
                            dbc.Row([
                                dbc.Label("Tag Gerador: "),
                                dcc.Dropdown(id="dropdown_tag_gerador_atualizar_paradas", options=popular_dropdown_gerador_atualizar_parada(), value=df_atual["EqpGerador"][0]),
                                dbc.Button("Adicionar Tag Gerador", id="adicionar_tag", style={"margin": "10px", "padding": "10px", "width": "90%"})
                            ]),

                            dbc.Row([
                                dbc.Label("Tipo de código: "),
                                dcc.Dropdown(id="dropdown_tipo_codigo_atualizar_paradas", options=popular_dropdown_tipo_de_codigo_atualizar_parada(), value=df_atual["TipoCodigo"][0])
                            ]),

                            dbc.Row([
                                dbc.Label("Grupo de Código: "),
                                dcc.Dropdown(id="dropdown_grupo_codigo_atualizar_paradas", options=[], value=df_atual["GrupoCodigo"][0])
                            ]),

                            dbc.Row([
                                dbc.Label("Código da Falha: "),
                                dcc.Dropdown(id="dropdown_codigo_falha_atualizar_paradas", options=[], value=df_atual["CodigoFalha"][0]),
                                dbc.Button("Adicionar Código da Falha", id="adicionar_codigo_falha", style={"margin": "10px", "padding": "10px", "width": "90%"})
                            ]),

                            dbc.Row([
                                dbc.Label("Causa Aparente: "),
                                dcc.Dropdown(id="dropdown_causa_aparente_paradas", options=[], value=df_atual["CausaAparente"][0]),
                                dbc.Button("Adicionar Causa Aparente", id="adicionar_causa_aparente", style={"margin": "10px", "padding": "10px", "width": "90%"})
                            ]),

                            dbc.Row([
                                dbc.Label("Componente: "),
                                dcc.Dropdown(id="dropdown_componente_atualizar_paradas", options=[], value=df_atual["Componente"][0]),
                                dbc.Button("Adicionar Componente", id="adicionar_componente", style={"margin": "10px", "padding": "10px", "width": "90%"})
                            ]),

                        ], style=card_style)
                    ]),

                dbc.Col([
                    dbc.Card([
                        html.Legend("Automático"),
                        dbc.Row([
                            dbc.Label("Processo: "),
                            dcc.Dropdown(id="dropdown_processo_paradas", options=popular_dropdown_processo_atualizar_parada(), value=df_atual["Producao"][0])
                        ]),

                        dbc.Row([
                            dbc.Label("Sistema: "),
                            dcc.Dropdown(id="dropdown_sistema_paradas", options=popular_dropdown_sistema_atualizar_parada(), value=df_atual["Sistema"][0])
                        ]),

                        dbc.Row([
                            dbc.Label("Equipamento: "),
                            dcc.Dropdown(id="equipamento_paradas", options=popular_dropdown_equipamento_atualizar_parada(), value=df_atual["Equipamento"][0])
                        ]),

                        dbc.Row([
                            html.Div([
                                html.Div([
                                    dbc.Col([dbc.Label("Início: ")]),
                                    dbc.Col([dcc.DatePickerSingle(id="dt_inicio_atualizar", display_format="DD/MM/YYYY", date=df_atual["DataInicio"][0])], style={"margin-right": '25px'}),
                                    dbc.Input(id="time_data_inicio_atualizar_parada", type="time", style={"width": "130px", "padding-top": "10px"}, value=hora_inicio)
                                ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin": "10px", "padding-top": "10px"}),
                                
                                html.Div([
                                    dbc.Col([dbc.Label("Fim: ")]),
                                    dbc.Col([dcc.DatePickerSingle(id="dt_fim_atualizar", display_format="DD/MM/YYYY", date=df_atual["DataFim"][0])], style={"margin-right": "25px"}),
                                    dbc.Input(id="time_data_fim_atualizar_parada", type="time", style={"width": "130px", "padding-top": "10px"}, value=hora_fim)
                                ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin": "10px", "padding-top": "10px"})
                                
                            ], style={"display": "flex", "flex-direction": "row", 'justify-content': "space-evenly", 'margin-top': '10px', 'padding-left': '10px'})
                        ]),

                        dbc.Row([
                            dbc.Label("Turno: "),
                            dcc.Dropdown(id="dropdown_turno_atualizar_paradas", options=dropdown_turno_atualizar_paradas(), value=df_atual["Turno"][0])
                        ]),

                        dbc.Row([
                            dbc.Label("Operador: "),
                            dcc.Dropdown(id="dropdown_operador_paradas", options=[username.replace("'","")], value=username.replace("'","")),
                            
                        ])
                    ],style=card_style)
                ])

                    
                ]),

                dbc.Row([

                    dbc.Col([
                        dbc.Card([
                            html.Legend("Manutenção"),

                            dbc.Row([
                                dbc.Label("Modo de falha: "),
                                dcc.Input(id="input_modo_falha_atualizar_parada", placeholder="Modo de Falha", type="text"),
                                dbc.Label("Apropriador: "),
                                dcc.Input(id="input_apropriador_atualizar_parada", placeholder="Apropriador", type="text"),
                                
                            ])  
                        ], style=card_style)
                    ]),

                    dbc.Col([
                        dbc.Card([
                            html.Legend("Observação"),

                            dbc.Row([
                            dcc.Input(id="input_observacao_paradas", placeholder="Observação", type="text")
                        ])
                        ], style=card_style),

                        
                    ]),

                    dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Cadastrar equipamento")),

                        dbc.ModalBody([
                            dcc.Dropdown(id="dd_modal_adicionar_processo", options=popular_processo_modal_adicionar_campo()),
                            dcc.Dropdown(id="dd_modal_adicionar_sistema", options=[]),
                            dcc.Dropdown(id="dd_modal_adicionar_grupo_equipamento", options=[]),
                            dbc.Input(id="input_modal_adicionar_equipamento", placeholder="Equipamento")
                        ]),

                        dbc.ModalFooter([
                            html.H4(id="gateway_cadastro_equip"),
                            dbc.Button("Cadastrar Equipamento", id="cadastrar_modal_cadastrar_equipamento")
                        ])
                    ], is_open=False, id="modal_adicionar_equipamento"),

                    dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Cadastrar Código da Falha")),

                        dbc.ModalBody([
                            dcc.Dropdown(id="dd_modal_adicionar_grupodecodigo", options=popular_grupo_codigo_modal_adicionar_campo()),
                            dbc.Input(id="input_modal_adicionar_codigofalha", placeholder="Código da Falha")
                        ]),

                        dbc.ModalFooter([
                            html.H4("", id="gateway_cadastro_codigofalha"),
                            dbc.Button("Cadastrar Código da Falha", id="cadastrar_modal_cadastrar_codigofalha")
                        ])
                    ], is_open=False, id="modal_adicionar_codigofalha"),

                    dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Cadastrar Causa Aparente")),

                        dbc.ModalBody([
                            dcc.Dropdown(id="dd_modal_adicionar_causaaparente", options=popular_causa_aparente_modaladicionar()),
                            dbc.Input(id="input_modal_adicionar_causaaparente", placeholder="Causa Aparente")
                        ]),

                        dbc.ModalFooter([
                            html.H4("", id="gateway_cadastro_causaaparente"),
                            dbc.Button("Cadastrar Causa Aparente", id="cadastrar_modal_cadastrar_causaparente")
                        ])
                    ], is_open=False, id="modal_adicionar_causa_aparente"),

                    dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Cadastrar Componente")),

                        dbc.ModalBody([
                            dcc.Dropdown(id="dd_modal_adicionar_componente", options=popular_componente_modaladicionar()),
                            dbc.Input(id="input_modal_adicionar_componente", placeholder="Componente")
                        ]),

                        dbc.ModalFooter([
                            html.H4("", id="gateway_cadastro_componente"),
                            dbc.Button("Cadastrar Componente", id="cadastrat_modal_cadastrar_componente")
                        ])
                    ], is_open=False, id="modal_adicionar_componente")

                ]),

                dbc.Row([
                    dbc.Col([
                        dbc.Button("Atualizar Parada", id="atualizar_final"),
                    ])
                ])

               

            ], style={"display": 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'margin-left': "10px"})
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return template


@app.callback(
    Output("dropdown_grupo_codigo_atualizar_paradas", "options"),
    Input("dropdown_tipo_codigo_atualizar_paradas", "value")
)
def popular_dropdown_grupo_codigo_atualizar_parada(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select [Grupo de Código] from tbl_GrupoDeCódigo where [Tipo de Código] = '{value}'"
        df_grupo_codigo = DataFrame(read_sql(ins, conn))

        arr = []

        for i in df_grupo_codigo.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr

@app.callback(
    Output("dropdown_codigo_falha_atualizar_paradas", "options"),
    Input("dropdown_grupo_codigo_atualizar_paradas", "value"),
)
def popular_dropdown_codigo_falha_paradas(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select [Código das Falhas] from tbl_CódigoDasFalhas where [Grupo de Código] = '{value}'"
        connect = engine.connect()
        df_codigo_falha = DataFrame(read_sql(ins, connect))

        arr = []

        for i in df_codigo_falha.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])
        connect.close()
        return arr

@app.callback(
    Output("dropdown_causa_aparente_paradas", "options"),
    Input("dropdown_codigo_falha_atualizar_paradas", "value")
)
def popular_dropdown_causa_aparente_atualizar(value):
    if value is None:
        raise PreventUpdate
    elif value is not None:
        ins = f"select CausaAparente from tbl_CausaAparente where CodigoFalha = '{value}'"
        connect = engine.connect()
        df_causa_aparente = DataFrame(read_sql(ins, connect))

        arr = []

        for i in df_causa_aparente.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        connect.close()

        return arr

@app.callback(
    Output("dropdown_componente_atualizar_paradas", "options"),
    Input("dropdown_tag_gerador_atualizar_paradas", "value")
)
def popular_dropdown_componente_atualizar_paradas(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select Componente from tbl_Componente comp inner join tbl_Equipamento equip on equip.[Grupo de Equipamentos] = comp.[Grupo de Equipamentos]"
        df_componente = DataFrame(read_sql(ins, engine.connect()))

        arr = []

        for i in df_componente.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr

# @app.callback(
#     Output("modal_aducionar_campo_atualizar", "is_open"),
#     Output("modal_aducionar_campo_atualizar", "children"),
#     Input("botao_adicionar_campos", "n_clicks"),
#     Input("h4_modal_nova_coluna", "children"),
#     State("modal_aducionar_campo_atualizar", "is_open"),
# )
# def controlar_modal_adicionar_campo_atualizar_parada(n, value, is_open):
#     item = [
#             dbc.ModalHeader(dbc.ModalTitle("Adicionar campo")),
#                                         dbc.ModalBody([
#                                             dcc.Dropdown(id="dropdown_modal_adicionar_campo_atualizar_paradas", options=[
#                                                 {'label': 'Equipamento', 'value': 'tbl_Equipamento'},
#                                                 {'label': 'Código das Falhas', 'value': "tbl_CódigoDasFalhas"},
#                                                 {"label": "Causa Aparente", 'value': "tbl_CausaAparente"},
#                                                 {"label": "Componente", 'value': "tbl_Componente"}
#                                             ]),
#                                             html.Div([

#                                             ], id="div_adaptativa_modal_adicionar_campo", style={"display": "flex", "flex-direction": "column", "justify-content": "start", "margin": '10px', "padding-top": "10px"})
#                                         ]),
#                                         dbc.ModalFooter([
#                                             html.H4(id="h4_modal_nova_coluna"),
#                                             dbc.Button("Cadastrar", id="cadastrar_modal_nova_coluna")
#                                         ])
#         ]

#     if n:
#         return not is_open, item
#     if value == "Campo adicionado":
#         return not is_open, item
#     return is_open, item


# @app.callback(
#     Output("div_adaptativa_modal_adicionar_campo", "children"),
#     Input("dropdown_modal_adicionar_campo_atualizar_paradas", "value")
# )
# def controlar_conteudo_modal(value):
#     if value is None:
#         raise PreventUpdate
#     else:
#         if value == "tbl_Equipamento":
#             item = [
#                 dcc.Dropdown(id="dd_modal_adicionar_campo_processo", options=popular_processo_modal_adicionar_campo()),
#                 dcc.Dropdown(id="dd_modal_adicionar_campo_sistema", options=popular_sistema_modal_adicionar_campo()),
#                 dcc.Dropdown(id="dd_modal_adicionar_campo_grupo_equipamento", options=popular_grupo_equipamento_modal_adicionar_campo()),
#                 dbc.Input(id="input_modal_adicionar_campo_equipamento", placeholder="Equipamento")
#             ]
#         if value == "tbl_CódigoDasFalhas":
#             item = [
#                 dcc.Dropdown(id="dd_modal_adicionar_campo_grupo_codigo", options=popular_grupo_codigo_modal_adicionar_campo()),
#                 dbc.Input(id="input_modal_adicionar_campo_codigo_falha", placeholder="Código das Falhas")
#             ]
#         if value == "tbl_CausaAparente":
#             item = [
#                 dcc.Dropdown(id="dd_modal_adicionar_campo_codigo_falha", options=popular_codigo_falha_modal_adicionar_campo()),
#                 dbc.Input(id="input_modal_adicionar_campo_causa_aparente", placeholder="Causa Aparente")
#             ]
#         if value == "tbl_Componente":
#             item = [
#                 dcc.Dropdown(id="dd_modal_adicionar_campo_grupo_equipamentos", options=popular_grupo_equipamentos_modal_adicionar_campo()),
#                 dbc.Input(id="input_modal_adicionar_campo_componente", placeholder="Componente")
#             ]
    
#         return item

@app.callback(
    Output("dd_modal_adicionar_sistema", "options"),
    Input("dd_modal_adicionar_processo", "value")
)
def popular_modal_adicionar_sistema(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select Sistema from tbl_Equipamento where Processo = '{value}'"
        df = DataFrame(read_sql(ins, conn))
        arr = []

        for i in df.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr

@app.callback(
    Output("dd_modal_adicionar_grupo_equipamento", "options"),
    Input("dd_modal_adicionar_sistema", "value"),
    State("dd_modal_adicionar_processo", "value")
)
def popular_modal_adicionar_grupo_equipamento(value, value2):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select [Grupo de Equipamentos] from tbl_Equipamento where Sistema = '{value}' and Processo = '{value2}'"
        df=DataFrame(read_sql(ins, engine.connect()))
        arr = []

        for i in df.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr 

@app.callback(
    Output("modal_adicionar_equipamento", "is_open"),
    Input("adicionar_tag", "n_clicks"),
    State("modal_adicionar_equipamento", "is_open")
)
def controlar_modal_adicionar_equip(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("gateway_cadastro_equip", "children"),
    Input("cadastrar_modal_cadastrar_equipamento", "n_clicks"),
    [
        State("dd_modal_adicionar_processo", "value"),
        State("dd_modal_adicionar_sistema", "value"),
        State("dd_modal_adicionar_grupo_equipamento", "value"),
        State("input_modal_adicionar_equipamento", "value")
    ]
)
def cadastrar_equip(n, proc, sist, gp_equip, equip):
    if n is None:
        raise PreventUpdate
    else:
        ins = f"insert into tbl_Equipamento (Processo, Sistema, [Grupo de Equipamentos], Equipamento) values ('{proc}', '{sist}', '{gp_equip}', '{equip}')"
        try:
            with engine.connect() as conn:
                conn.execute(text(ins))
                conn.commit()
                conn.close()
            return 'Dados cadastrados'
        except:
            "Erro"

@app.callback(
    Output("modal_adicionar_codigofalha", "is_open"),
    Input("adicionar_codigo_falha", "n_clicks"),
    State("modal_adicionar_codigofalha", "is_open")
)
def controlar_modal_codigofalha(n, is_open):
    if n is not None:
        return not is_open
    return is_open

@app.callback(
    Output("gateway_cadastro_codigofalha", "children"),
    Input("cadastrar_modal_cadastrar_codigofalha", "n_clicks"),
    [
        State("dd_modal_adicionar_grupodecodigo", "value"),
        State("input_modal_adicionar_codigofalha", "value")
    ]
)
def cadastrar_codigofalha(n, value1, value2):
    if n is None:
        raise PreventUpdate
    else:
        ins = f"insert into tbl_CódigoDasFalhas ([Grupo de Código], [Código das Falhas]) values ('{value1}', '{value2}')"
        try:
            with engine.connect() as conn:
                conn.execute(text(ins))
                conn.commit()
                conn.close()
            return 'Dados cadastrados'
        except:
            "Erro"

@app.callback(
    Output("modal_adicionar_causa_aparente", "is_open"),
    Input("adicionar_causa_aparente", "n_clicks"),
    State("modal_adicionar_causa_aparente", "is_open")
)
def controlar_modal_causa_aparente(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("gateway_cadastro_causaaparente", "children"),
    Input("cadastrar_modal_cadastrar_causaparente", "n_clicks"),
    [
        State("dd_modal_adicionar_causaaparente", "value"),
        State("input_modal_adicionar_causaaparente", "value")
    ]
)
def cadastrar_modal_causaaparente(n, value1, value2):
    if n is None:
        raise PreventUpdate
    else:
        ins = f"insert into tbl_CausaAparente (CodigoFalha, CausaAparente) values ('{value1}', '{value2}')"
        try:
            with engine.connect() as conn:
                conn.execute(text(ins))
                conn.commit()
                conn.close()
            return 'Dados cadastrados'
        except:
            "Erro"

@app.callback(
    Output("modal_adicionar_componente", "is_open"),
    Input("adicionar_componente", "n_clicks"),
    State("modal_adicionar_componente", "is_open")
)
def controlar_modal_componente(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("gateway_cadastro_componente", "children"),
    Input("cadastrat_modal_cadastrar_componente", "n_clicks"),
    [
        State("dd_modal_adicionar_componente", "value"),
        State("input_modal_adicionar_componente", "value")
    ]
)
def cadastrar_componente(n, value1, value2):
    if n is None:
        raise PreventUpdate
    else:
        ins = f"insert into tbl_Componente ([Grupo de Equipamentos], Componente) values ('{value1}', '{value2}')"
        try:
            with engine.connect() as conn:
                conn.execute(text(ins))
                conn.commit()
                conn.close()
            return 'Dados cadastrados'
        except:
            "Erro"

@app.callback(
    Output("atualizar_paradas_base_url", "pathname"),
    Input("atualizar_final", "n_clicks"),
    [
        State("atualizar_paradas_base_url", "pathname"),
        State("dropdown_tipo_codigo_atualizar_paradas", "value"),
        State("dropdown_grupo_codigo_atualizar_paradas", "value"),
        State("dropdown_codigo_falha_atualizar_paradas", "value"),
        State("dropdown_causa_aparente_paradas", "value"),
        State("dropdown_componente_atualizar_paradas", "value"),
        State("dropdown_processo_paradas", "value"),
        State("dropdown_sistema_paradas", "value"),
        State("equipamento_paradas", "value"),
        State("dt_inicio_atualizar", "date"),
        State("time_data_inicio_atualizar_parada", "value"),
        State("dt_fim_atualizar", "date"),
        State("time_data_fim_atualizar_parada", "value"),
        State("dropdown_turno_atualizar_paradas", "value"),
        State("dropdown_operador_paradas", "value"),
        State("input_modo_falha_atualizar_parada", "value"),
        State("input_apropriador_atualizar_parada", "value"),
        State("input_observacao_paradas", "value")
    ]
)
def atualizar_parada_final(n, pathname, tipo_codigo, grupo_codigo, codigo_falha, causa_aparente, componente, processo, sistema, equipamento, dt_inicio, hr_inicio, dt_fim, hr_fim, turno, operador, modo_falha, apropriador, obs):
    if n is None:
        raise PreventUpdate
    else:
        id = pathname[18:]
        ins = "update tbl_Paradas set "

        dt_inicio = str(dt_inicio)[:10]
        dt_fim = str(dt_fim)[:10]

        if tipo_codigo:
            ins += f"TipoCodigo = '{tipo_codigo}',"
        if grupo_codigo:
            ins += f"GrupoCodigo = '{grupo_codigo}',"
        if codigo_falha:
            ins += f"CodigoFalha = '{codigo_falha}',"
        if causa_aparente:
            ins += f"CausaAparente = '{causa_aparente}',"
        if componente:
            ins += f"Componente = '{componente}',"
        if processo:
            ins += f"Producao = '{processo}',"
        if sistema:
            ins += f"Sistema = '{sistema}',"
        if equipamento:
            ins += f"Equipamento = '{equipamento}',"
        if dt_inicio:
            ins += f"DataInicio = '{dt_inicio} {hr_inicio}',"
        if dt_fim:
            ins += f"DataFim = '{dt_fim} {hr_fim}',"
        if turno:
            ins += f"Turno = '{turno}',"
        if operador:
            ins += f"Operador = '{operador}',"
        if modo_falha:
            ins += f"ModoFalha = '{modo_falha}',"
        if apropriador:
            ins += f"Apropriador = '{apropriador}',"
        if obs:
            ins += f"Observacao = '{obs}',"

        ins = ins[:-1]
        ins += f"where Id = {id}"

        try:
            with engine.connect() as conn:
                conn.execute(text(ins))
                conn.commit()
                conn.close()
            return '/consultar_paradas'
        except:
            return f'/atualizar_parada/{id}'
