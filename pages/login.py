from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import *
from dash.exceptions import PreventUpdate
from werkzeug.security import check_password_hash
from flask_login import login_user
from sqlalchemy import text
from sqlalchemy.orm import Session

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
    'flex-direction': 'column',
    'background-color': 'white',
    'border-radius': '5px',
    'font-family': 'sans-serif',
    'font-style': 'bold',
    'justify-content': 'space-evenly'
}

def render_layout(login_state):
    message = ''
    if login_state == 'error':
        message = 'Ocorreu algum erro'
    elif login_state == 'error_senha':
        message = 'Senha incorreta'
    elif login_state == 'error_nao_encontrado':
        message = 'Usuário não existe'

    login = dbc.Card([
        html.Div([
            html.Img(src=app.get_asset_url("mvv-logo.png"), height=70, width=180),
        ], style={"padding": "5px", "justify-content": "center", "display": "flex"}),
        html.Div([
            dbc.Input(id="user_login", placeholder="Usuário", type="text", style={"margin-bottom": '10px'}),
            dbc.Input(id="password_login", placeholder="Senha", type="password", style={"margin-bottom": '10px'}),
            dbc.Button("Login", id="login_button"),
        ], style={'display': 'flex', "flex-direction": 'column', 'justify-content': 'space-evenly', "margin": "10px", "padding": "10px"}),
        
        html.Span(message, style={"text-align": 'center'}),
       
    ], style=card_style)

    return login

@app.callback(
    Output("login_state", "data"),
    Input("login_button", "n_clicks"),
    [
        State("user_login", "value"),
        State("password_login", "value")
    ]
)
def logar(n_clicks, user_login, password_login):
    if n_clicks == None:
        raise PreventUpdate

    try:
        session = Session(engine)
        rst = session.query(User).filter(User.nm_usr==f"'{text(user_login)}'")
        user = rst[0]
        # user = User.query.filter_by(nm_usr=f"'{text(user_login)}'").first()
        if user and password_login is not None:
            if check_password_hash(user.pwd_usr.replace("'", ""), password_login):
                login_user(user)
                return 'success'
            else:
                return 'error_senha'
        else:
            return 'error'
    except:
        return 'error_nao_encontrado'