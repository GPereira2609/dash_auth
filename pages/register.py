from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import *

import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px

from werkzeug.security import generate_password_hash
from sqlalchemy import text
from dash.exceptions import PreventUpdate
from app import *

card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column',
    'padding': '10px'
}

def render_layout(register_state):
    message = ''
    if register_state == 'error':
        message = "Ocorreu algum erro"
    elif register_state == 'error_usuario_existente':
        message = "O usuário ou email utilizado já existe"
    else:
        message
    
    register = dbc.Card([
        html.Div([
            html.H3("Registro"),
        ], style={"padding": "5px", "justify-content": "center", "display": "flex"}),
        dbc.Input(id="user_register", placeholder="Usuário", type="text"),
        dbc.Input(id="password_register", placeholder="Senha", type="password"),
        dbc.Input(id="email_register", placeholder="Email", type="email"),
        dbc.Button("Registrar", id="register_button"),
        html.Span(message, style={"text-align": 'center'}),
        html.Div([
            html.Label("Ou", style={"margin-right": "5px"}),
            dcc.Link("Login", href="/login")
        ], style={"padding": "20px", "justify-content": "center", "display": "flex"})

    ], style=card_style)

    return register

@app.callback(
    Output('register_state', 'data'),
    Input('register_button', 'n_clicks'),
    [
        State('user_register', 'value'),
        State('password_register', 'value'),
        State('email_register', 'value')
    ]
)
def registrar_usuario(n_clicks, user_register, password_register, email_register):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        try:
            if (user_register is None) or (password_register is None) or (email_register is None):
                return 'error'
            elif (user_register and password_register, email_register) is not None:
                hashed_password = generate_password_hash(password_register, method="SHA256")
                ins = Users_table.insert().values(nm_usr=f"'{user_register}'", pwd_usr=f"'{hashed_password}'", email_usr=f"'{email_register}'")
                # print(ins)
                # ins = f"insert into usuarios (nm_usr, email_usr, pwd_usr) values ('{user_register}', '{email_register}', '{hashed_password}')"
                conn = engine.connect()
                conn.execute(ins)
                conn.commit()
                conn.close()
                return ''
        except:
            return 'error_usuario_existente'
       