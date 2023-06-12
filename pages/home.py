from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import *
from dash.exceptions import PreventUpdate
from flask_login import current_user, logout_user
from functools import wraps
from app import *
from flask import redirect

from pages import navbar
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
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
	  dcc.Location(id="home_base_url"),
        navbar.nav()[0],
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

