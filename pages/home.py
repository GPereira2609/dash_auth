from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import *
from dash.exceptions import PreventUpdate
from flask_login import current_user, logout_user
from functools import wraps
from app import *
from flask import redirect

from pages import sidebar
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px

card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}

# def admin_required(func):
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         if current_user.usr_role != 'admin':
#             return ''
#         return func(*args, **kwargs)
#     return decorated_view

def render_layout(user):
    username = user.nm_usr
    username = username.replace("'", "")

    template = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Col([
                            html.Img(src=app.get_asset_url('do-utilizador.png'), height=70, width=70), 
                        ], style={"display": "flex", "flex-direction": "column", "justify-content": "center"}),
                        dcc.Location(id="home_base_url"),
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
                html.H1("Bem Vindo ao Sistema de Controle e Apropriação de Paradas", style={"font-family": "sans-serif"}, id="h1"),
                # dbc.Button("Sair", "botao_logout")
            ], style={"display": 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'})
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return template

# @app.callback(
#     Output("home_base_url", "pathname"),
#     Input("botao_logout", "n_clicks")
# )
# def deslogar(n):
#     if n is None:
#         raise PreventUpdate
#     if n is not None:
#         if current_user.is_authenticated:
#             logout_user()
#             return '/login'
#         else:
#             return '/login'

