import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from app import *
from flask_login import logout_user
from dash.exceptions import PreventUpdate

card_style = {
    'margin-top': '25px',
    'width': '500px',
    'height': '50px',
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
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Col([
                            html.Img(src=app.get_asset_url('do-utilizador.png'), height=70, width=70), 
                        ], style={"display": "flex", "flex-direction": "column", "justify-content": "center"}),
                        dcc.Location(id="aprop_turno_base_url"),
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
                                dcc.Dropdown(id="dropdown_processo_turno", options=["sql"])
                            ]),

                            dbc.Row([
                                dbc.Label("Sistema: "),
                                dcc.Dropdown(id="dropdown_sistema_turno", options=["sql"])
                            ]),

                            dbc.Row([
                                dbc.Label("Equipamento: "),
                                dcc.Dropdown(id="dropdown_equipamento_turno", options=["sql"])
                            ]),

                            dbc.Row([
                                html.Div([
                                    dbc.Col(dbc.Label("Data: ")),
                                    dbc.Col(dcc.DatePickerSingle(display_format="DD/MM/YYYY"))
                                ], style={'display': 'flex', 'flex-direction': 'column', 'margin-top': '10px', 'padding-left': '10px'})
                            ])
                        ], style=card_style)
                    ])
                ])
            ], style={"display": 'flex', 'flex-direction': 'column', 'justify-content': 'center', "margin-left": "10px"})
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return template

