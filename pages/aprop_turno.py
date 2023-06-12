import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from app import *
from flask_login import logout_user
from dash.exceptions import PreventUpdate
from pages import navbar

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
        navbar.nav()[0],
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

