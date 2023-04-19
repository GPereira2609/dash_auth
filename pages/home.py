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
                html.Div([
                    html.Div([
                    dcc.Location(id="base_url"),
                    html.H3(f"{username} ({user.usr_role})", style={"color": "white"}),
                    dbc.Button("Logout", style={"border-radius": "8px", 'width': '100px'}, id="botao_logout")
                ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'height': "100%"}),

                html.Div(dbc.Row(dbc.Col())),

                html.Div([
                    dbc.Nav([
                        dbc.NavLink("Home", href="/home", active="exact"),
                        dbc.NavLink("Consultar paradas", href="/consultar_paradas", active="exact"),
                        dbc.NavLink("Apropriar paradas", href="/aprop_paradas", active="exact"),
                        dbc.NavLink("Consultar turno", href="/consultar_turno", active="exact"),
                        dbc.NavLink("Apropriação turno", href="/aprop_turno", active="exact")
                    ], pills=True, vertical=False, id='nav')
                ], style={"height": "100%", 'display': 'flex', 'flex-direction': 'column'}),

                html.Div(dbc.Row(dbc.Col())),

                html.Div([
                    html.Img(src=app.get_asset_url('f2711217-e0a9-4a63-a24c-3c969b7ce090.png'), height=75, width=194)
                ])
                ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}),
                
            ], style={"height": '15%', 'width': '110vw', 'display': 'flex', 'flex-direction': "column", 'justify-content': 'space-evenly', 'background-color': '#298753'}),

        dbc.Row([   
            html.Div([
                html.H1("Bem Vindo ao Sistema de Controle e Apropriação de Paradas", style={"font-family": "sans-serif"}, id="h1"),
            ], style={"display": 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'})
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return template

@app.callback(
    Output("base_url", "pathname"),
    Input("botao_logout", "n_clicks")
)
def deslogar(n):
    if n is None:
        raise PreventUpdate
    if n is not None:
        logout_user()
        return '/login'

