import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, Input, Output
from app import *
from dash.exceptions import PreventUpdate
from flask_login import logout_user
from pages import navbar

card_style = {
    'width': '500px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}

card_style2= {
    'width': '1120px',
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
    
    template = html.Div([
            navbar.nav()[0],
            dbc.Row([   
                html.Div([
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.Legend("Processo/equipamento"),
                                dbc.Row([
                                    dbc.Label("Processo: "),
                                    dcc.Dropdown(options=["Via seca", "via umida", "SQL"], id="dropdown_processo")
                            ]),
                                dbc.Row([
                                    dbc.Label("Sistema: "),
                                    dcc.Dropdown(options=["Via seca", "via umida", "SQL"], id="dropdown_sistema")
                            ]),
                                dbc.Row([
                                    dbc.Label("Equipamento: "),
                                    dcc.Dropdown(options=["Via seca", "via umida", "SQL"], id="dropdown_equipamento")
                            ]),
                                dbc.Row([
                                    dcc.Input(id="input_descricao_turno", placeholder="Descrição da ocorrência", style={"margin": '10px', 'border': 'grey', 'placeholder::color': 'grey'})
                                ])
                            ], style=card_style),
                            
                            ]),

                        dbc.Col([
                            dbc.Card([
                                html.Legend("Período"),
                                dbc.Row([
                                    dbc.Label("Início: "),
                                    dcc.DatePickerSingle(display_format="DD/MM/YYYY")
                            ]),

                                dbc.Row([
                                    dbc.Label("Fim: "),
                                    dcc.DatePickerSingle(display_format="DD/MM/YYYY")
                            ]),

                                dbc.Row([
                                    dbc.Button("Consultar", id="botao_consultar_turnos", style={"margin": "10px", 'width': '100px'})
                                ])
                            ], style=card_style),
                            
                        ])
                        ], style={"padding-top": "25px"}),

                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    html.Legend("Dados"),
                                    dbc.Row([
                                        dbc.Label("Dados"),
                                        dash_table.DataTable(id="tabela_dados")
                                    ])
                                ], style=card_style2)
                            ])
                        ], style={"padding-top": "25px"})
                        

                    ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin-left": "10px"})


            ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
        ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return template
