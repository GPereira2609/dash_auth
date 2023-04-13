from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import *
from dash.exceptions import PreventUpdate
from flask_login import current_user, logout_user
from functools import wraps

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

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != 'admin':
            return '/home'
        return func(*args, **kwargs)
    return decorated_view

def render_layout(username):
    template = dbc.Card([
        dcc.Location(id="data_url"),
        html.Legend(f"Olá {username}"),
        dbc.Button("Botão adm", id="b1"),
        dbc.Button("Botão normal", id="b2"),
        html.H1(id="h1"),
        dbc.Button("Logout", id='b_logout', href='/login')
    ], style=card_style)

    return template

@app.callback(
    Output("h1", "children"),
    Input("b1", "n_clicks"),
    Input('b2', "n_clicks"),
    Input("b_logout", "n_clicks")
)
@admin_required
def botoes(n1, n2, n_logout):
    if (n1 or n2 or n_logout) is None:
        raise PreventUpdate
    if n1 is not None:
        if current_user.usr_role == 'admin':
            print('here')
            return "vc é admin"
        else:
            print('not, here')
            return 'vc n é admin'
    if n2 is not None:
        return 'você tem permissões de operador'

    if n_logout is not None:
        logout_user(current_user)
        return ''

