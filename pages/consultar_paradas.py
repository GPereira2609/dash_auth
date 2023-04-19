from app import *
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output
from dash.exceptions import PreventUpdate
from flask_login import logout_user

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
    
    layout = html.Div([
            dbc.Row([
                html.Div([
                    html.Div([
                    dcc.Location(id="base_url"),
                    html.H3(username.replace("'", ""), style={"color": "white"}),
                    
                ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'height': "100%"}),

                    html.Div([
                        dbc.Nav([
                            dbc.NavLink("Home", href="/home", active="exact"),
                            dbc.NavLink("Consultar paradas", href="/consultar_paradas", active="exact"),
                            dbc.NavLink("Apropriar paradas", href="/aprop_paradas", active="exact"),
                            dbc.NavLink("Consultar turno", href="/consultar_turno", active="exact"),
                            dbc.NavLink("Apropriação turno", href="/aprop_turno", active="exact")
                        ], pills=True, vertical=False, id='nav')
                    ], style={"height": "100%", 'display': 'flex', 'flex-direction': 'column'}),

                    html.Div([
                        html.Img(src=app.get_asset_url('f2711217-e0a9-4a63-a24c-3c969b7ce090.png'), height=75, width=194)
                    ])
                ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}),
                
            ], style={"height": '15%', 'width': '110vw', 'display': 'block', 'justify-content': 'space-evenly', 'background-color': '#298753'}),

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
                                        dbc.Label("Dados"),
                                        dash_table.DataTable(id="tabela_dados")
                                    ])
                                ], style=card_style2)
                            ])
                        ], style={"padding-top": "25px"})
                        

                    ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin-left": "10px"})


            ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
        ], style={'background-color': "white", 'height': '100vh', 'width': '100vw', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'width': '100vw'})
        
    return layout
