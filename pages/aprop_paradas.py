import dash_bootstrap_components as dbc
from dash import dcc, html, Input,Output, State
from app import *
from flask_login import logout_user
from dash.exceptions import PreventUpdate
from globals import *
from pages import navbar

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

def render_layout(user):
    username = user.nm_usr

    template = html.Div([
        navbar.nav()[0],
        dbc.Row([   
            html.Div([
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.Legend("Operação"),
                            dbc.Row([
                                dbc.Label("Tag Gerador: "),
                                dcc.Dropdown(id="dropdown_tag_gerador_paradas", options=popular_gerador_aprop_paradas()),
                            ]),

                            dbc.Row([
                                dbc.Label("Tipo de código: "),
                                dcc.Dropdown(id="dropdown_tipo_codigo_paradas", options=popular_tipocodigo_aprop_paradas())
                            ]),

                            dbc.Row([
                                dbc.Label("Grupo de Código: "),
                                dcc.Dropdown(id="dropdown_grupo_codigo_paradas", options=[])
                            ]),

                            dbc.Row([
                                dbc.Label("Código da Falha: "),
                                dcc.Dropdown(id="dropdown_codigo_falha_paradas", options=[])
                            ]),

                            dbc.Row([
                                dbc.Label("Causa Aparente: "),
                                dcc.Dropdown(id="dropdown_causa_aparente_aprop_paradas", options=[])
                            ]),

                            dbc.Row([
                                dbc.Label("Componente: "),
                                dcc.Dropdown(id="dropdown_componente_paradas", options=["Chapa de Desgaste", "sql"])
                            ]),

                            
                        ], style=card_style)
                    ]),

                dbc.Col([
                    dbc.Card([
                        html.Legend("Automático"),
                        dbc.Row([
                            dbc.Label("Processo: "),
                            dcc.Dropdown(id="dropdown_processo_paradas", options=popular_aprop_paradas_processo())
                        ]),

                        dbc.Row([
                            dbc.Label("Sistema: "),
                            dcc.Dropdown(id="dropdown_sistema_paradas", options=popular_aprop_paradas_sistema())
                        ]),

                        dbc.Row([
                            dbc.Label("Equipamento: "),
                            dcc.Dropdown(id="equipamento_paradas", options=popular_aprop_paradas_equip())
                        ]),

                        dbc.Row([
                            html.Div([
                                html.Div([
                                    dbc.Col([dbc.Label("Início: ")]),
                                    dbc.Col([dcc.DatePickerSingle(display_format="DD/MM/YYYY")], style={"margin-right": '25px'}, id="data_inicio_aprop_paradas"),
                                    dbc.Col([dbc.Input(id="time_inicio_aprop_paradas", type="time", style={"width": "130px", "padding-top": "10px"})])
                                ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin": "10px", "padding-top": "10px"}),
                                html.Div([
                                    dbc.Col([dbc.Label("Fim: ")]),
                                    dbc.Col([dcc.DatePickerSingle(display_format="DD/MM/YYYY")], style={"margin-right": "25px"}, id="data_fim_aprop_paradas"),
                                    dbc.Col([dbc.Input(id="time_fim_aprop_paradas", type="time", style={"width": "130px", "padding-top": "10px"})])
                                ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin": "10px", "padding-top": "10px"})
                                
                            ], style={"display": "flex", "flex-direction": "row", 'justify-content': "space-evenly", 'margin-top': '10px', 'padding-left': '10px'})
                        ]),

                        dbc.Row([
                            dbc.Label("Turno: "),
                            dcc.Dropdown(id="dropdown_turno_paradas", options=popular_aprop_paradas_turno())
                        ]),

                        dbc.Row([
                            dbc.Label("Operador: "),
                            dcc.Dropdown(id="dropdown_operador_paradas", options=[username.replace("'", "")]),
                            
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
                                dbc.Input(id="input_modo_falha_paradas", placeholder="Modo de Falha"),
                                
                            ]),

                            dbc.Row([
                                dbc.Label("Apropriador: "),
                                dbc.Input(id="input_apropriador_paradas", placeholder="Apropriador")
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

                        
                    ])

                ]),

                dbc.Row([
                    html.Div([

                        dbc.Button("Cadastrar", id="cadastro_aprop_paradas", style={"width": "150px"}),
                        html.H4(id="gateway_aprop_paradas")
                    ], style={"display": "flex", "flex-direction": "column"})
                    ])

               

            ], style={"display": 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'margin-left': "10px"})
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return template

@app.callback(
    Output("dropdown_grupo_codigo_paradas", "options"),
    Input("dropdown_tipo_codigo_paradas", "value")
)
def popular_grupocodigo_aprop_paradas(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select [Grupo de Código] from tbl_GrupoDeCódigo where [Tipo de Código] = '{value}'"
        df = DataFrame(read_sql(ins, engine.connect()))

        arr = []

        for i in df.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr

@app.callback(
    Output("dropdown_codigo_falha_paradas", "options"),
    Input("dropdown_grupo_codigo_paradas", "value")
)
def popular_codigofalha_aprop_paradas(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select [Código das Falhas] from tbl_CódigoDasFalhas where [Grupo de Código] = '{value}'"
        df = DataFrame(read_sql(ins, engine.connect()))

        arr = []

        for i in df.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr

@app.callback(
    Output("dropdown_causa_aparente_aprop_paradas", "options"),
    Input("dropdown_codigo_falha_paradas", "value")
)
def popular_causaaparente_aprop_paradas(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select CausaAparente from tbl_CausaAparente where CodigoFalha = '{value}'"
        df = DataFrame(read_sql(ins, engine.connect()))

        arr = []

        for i in df.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr

@app.callback(
    Output("dropdown_componente_paradas", "options"),
    Input("dropdown_tag_gerador_paradas", "value")
)
def popular_componente_aprop_paradas(value):
    if value is None:
        raise PreventUpdate
    else:
        ins = f"select Componente from tbl_Componente inner join Tbl_Equipamento on tbl_Componente.[Grupo de Equipamentos] = tbl_Equipamento.[Grupo de Equipamentos] where tbl_Equipamento.Equipamento = '{value}'"
        df = DataFrame(read_sql(ins, engine.connect()))

        arr = []

        for i in df.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr

@app.callback(
    Output("gateway_aprop_paradas", "children"),
    Input("cadastro_aprop_paradas", "n_clicks"),
    [
        State("dropdown_tag_gerador_paradas", "value"),
        State("dropdown_tipo_codigo_paradas", "value"),
        State("dropdown_grupo_codigo_paradas", "value"),
        State("dropdown_codigo_falha_paradas", "value"),
        State("dropdown_causa_aparente_aprop_paradas", "value"),
        State("dropdown_componente_paradas", "value"),
        State("dropdown_processo_paradas", "value"),
        State("dropdown_sistema_paradas", "value"),
        State("equipamento_paradas", "value"),
        State("data_inicio_aprop_paradas", "date"),
        State("time_inicio_aprop_paradas", "value"),
        State("data_fim_aprop_paradas", "date"),
        State("time_fim_aprop_paradas", "value"),
        State("dropdown_turno_paradas", "value"),
        State("dropdown_operador_paradas", "value"),
        State("input_modo_falha_paradas", "value"),
        State("input_apropriador_paradas", "value"),
        State("input_observacao_paradas", "value")
    ]
)
def cadastrar_apropriacao(n, gerador, tipo_codigo, grupo_codigo, codigo_falha, causa_aparente, componente, processo, sistema, equipamento, dt_inicio, tm_inicio, dt_fim, tm_fim, turno, operador, modo_falha, apropriador, obs):
    ins1 = "insert into tbl_Paradas ("
    ins2 = ' values ('

    if n is None:
        raise PreventUpdate
    else:

        if gerador:
            ins1 += "EqpGerador,"
            ins2 += f"'{gerador}',"

        if tipo_codigo:
            ins1 += "TipoCodigo,"
            ins2 += f"'{tipo_codigo}',"

        if grupo_codigo:
            ins1 += "GrupoCodigo,"
            ins2 += f"'{grupo_codigo}',"

        if codigo_falha:
            ins1 += "CodigoFalha,"
            ins2 += f"'{codigo_falha}',"

        if causa_aparente:
            ins1 += "CausaAparente,"
            ins2 += f"'{causa_aparente}',"

        if componente:
            ins1 += "Componente,"
            ins2 += f"'{componente}',"

        if processo:
            ins1 += "Producao,"
            ins2 += f"'{processo}',"

        if sistema:
            ins1 += "Sistema,"
            ins2 += f"'{sistema}',"

        if equipamento:
            ins1 += "Equipamento,"
            ins2 += f"'{equipamento}',"

        if dt_inicio and tm_fim:
            ins1 += "DataInicio,"
            ins2 += f"'{dt_inicio} {tm_inicio}',"
        elif dt_inicio:
            ins1 += "DataInicio,"
            ins2 += f"'{dt_inicio}',"

        if dt_fim and tm_fim:
            ins1 += "DataFim,"
            ins2 += f"'{dt_fim} {tm_fim}',"
        elif dt_fim:
            ins1 += "DataFim,"
            ins2 += f"'{dt_fim}',"

        if turno:
            ins1 += "Turno,"       
            ins2 += f"'{turno}',"

        if operador:
            ins1 += "Operador," 
            ins2 += f"'{operador}',"

        if modo_falha:
            ins1 += "ModoFalha,"
            ins2 += f"'{modo_falha}',"

        if apropriador:
            ins1 += "Apropriador,"
            ins2 += f"'{apropriador}',"

        if obs:
            ins1 += "Observacao,"
            ins2 += f"'{obs}',"

        ins1 = ins1[:-1]
        ins2 = ins2[:-1]
        ins1 += ")"
        ins2 += ")"
        ins = ins1 + ins2

        try:
            with engine.connect() as conn:
                conn.execute(text(ins))
                conn.commit()
                conn.close()
            return 'Dados cadastrados'
        except:
            raise PreventUpdate