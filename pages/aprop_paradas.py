import dash_bootstrap_components as dbc
from dash import dcc, html, Input,Output
from app import *
from flask_login import logout_user
from dash.exceptions import PreventUpdate

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
        dbc.Row([
                html.Div([
                    html.Div([
                        dcc.Location(id="aprop_paradas_base_url"),
                    html.H3(username.replace("'", ""), style={"color": "white"}),
                    
                ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'height': "100%"}),

                    html.Div([
                        dbc.Nav([
                            dbc.NavLink("Home", href="/home", active="exact"),
                            dbc.NavLink("Consultar paradas", href="/consultar_paradas", active="exact"),
                            dbc.NavLink("Apropriar paradas", href="/aprop_paradas", active="exact"),
                            dbc.NavLink("Consultar turno", href="/consultar_turno", active="exact"),
                            dbc.NavLink("Apropriação turno", href="/aprop_turno", active="exact"),
                            dbc.NavLink("Registrar usuário", href="/register", active="exact")
                        ], pills=True, vertical=False, id='nav')
                    ], style={"height": "100%", 'display': 'flex', 'flex-direction': 'column'}),

                    html.Div([
                        html.Img(src=app.get_asset_url('f2711217-e0a9-4a63-a24c-3c969b7ce090.png'), height=75, width=194)
                    ])
                ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}),
                
            ], style={"height": '15%', 'width': '105vw', 'display': 'block', 'justify-content': 'space-evenly', 'background-color': '#298753'}),

        dbc.Row([   
            html.Div([
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.Legend("Operação"),
                            dbc.Row([
                                dbc.Label("Tag Gerador: "),
                                dcc.Dropdown(id="dropdown_tag_gerador_paradas", options=["2101-CH-001", "sql"]),
                            ]),

                            dbc.Row([
                                dbc.Label("Tipo de código: "),
                                dcc.Dropdown(id="dropdown_tipo_codigo_paradas", options=["Horas Paradas HP", "sql"])
                            ]),

                            dbc.Row([
                                dbc.Label("Grupo de Código: "),
                                dcc.Dropdown(id="dropdown_grupo_codigo_paradas", options=['Horas Paradas Externas HPE', 'sql'])
                            ]),

                            dbc.Row([
                                dbc.Label("Código da Falha: "),
                                dcc.Dropdown(id="dropdown_codigo_falha_paradas", options=["Parada Externa", "sql"])
                            ]),

                            dbc.Row([
                                dbc.Label("Causa Aparente: "),
                                dcc.Dropdown(id="dropdown_causa_aparente_paradas", options=["Incidente/Acidente", "sql"])
                            ]),

                            dbc.Row([
                                dbc.Label("Componente: "),
                                dcc.Dropdown(id="dropdown_componente_paradas", options=["Chapa de Desgaste", "sql"])
                            ]),

                            dbc.Row([

                                html.Div([
                                    dcc.Checklist(
                                    ["Próprio Equipamento"]
                                ),

                                    dbc.Button("Adicionar campo", id="botao_adicionar_campos", style={"width": "150px", 'padding-left': '10px'})
                                ], style={"display": "flex", "flex-direction": "row", "padding": "5px", 'margin-top': "10px", 'paddding-left': '10px'})
                                
                            ])
                        ], style=card_style)
                    ]),

                dbc.Col([
                    dbc.Card([
                        html.Legend("Automático"),
                        dbc.Row([
                            dbc.Label("Processo: "),
                            dcc.Dropdown(id="dropdown_processo_paradas", options=["sql"])
                        ]),

                        dbc.Row([
                            dbc.Label("Sistema: "),
                            dcc.Dropdown(id="dropdown_sistema_paradas", options=["sql"])
                        ]),

                        dbc.Row([
                            dbc.Label("Equipamento: "),
                            dcc.Dropdown(id="equipamento_paradas", options=["sql"])
                        ]),

                        dbc.Row([
                            html.Div([
                                dbc.Col([dbc.Label("Início: ")]),
                                dbc.Col([dcc.DatePickerSingle(display_format="DD/MM/YYYY")], style={"margin-right": '25px'}),
                                dbc.Col([dbc.Label("Fim: ")]),
                                dbc.Col([dcc.DatePickerSingle(display_format="DD/MM/YYYY")], style={"margin-right": "25px"})
                            ], style={"display": "flex", "flex-direction": "row", 'justify-content': "space-evenly", 'margin-top': '10px', 'padding-left': '10px'})
                        ]),

                        dbc.Row([
                            dbc.Label("Turno: "),
                            dcc.Dropdown(id="dropdown_turno_paradas", options=["sql"])
                        ]),

                        dbc.Row([
                            dbc.Label("Operador: "),
                            dcc.Dropdown(id="dropdown_operador_paradas", options=["sql"]),
                            html.Div([
                                dbc.Button("Adicionar campo", id="botao_adicionar_campos_2", style={"width": "150px"})
                            ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'margin-top': '10px'})
                            
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
                                dcc.Dropdown(id="dropdown_apropriador_paradas", options=["sql"]),
                                html.Div([
                                    dbc.Button("Adicionar campo", id="botao_adicionar_campos_3", style={"width": "150px"})
                                ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin-top": "10px"})
                                
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

                ])

               

            ], style={"display": 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'margin-left': "10px"})
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return template

