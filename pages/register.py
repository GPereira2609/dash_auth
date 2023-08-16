from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import *

import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import sqlite3

from werkzeug.security import generate_password_hash
from sqlalchemy import text
from dash.exceptions import PreventUpdate
from functools import wraps 
from flask_login import current_user

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if(current_user.is_authenticated):
            if (current_user.usr_role != 'aprop_admin') and (current_user.usr_role != "lab_pcp"):
                return ''
        return func(*args, **kwargs)
    return decorated_view

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

def render_layout(register_state):
    message = ''
    if register_state == 'error':
        message = "Ocorreu algum erro"
    elif register_state == "error_info":
        message = "Preencha todos os campos"
    elif register_state == 'error_usuario_existente':
        message = "O usuário ou email utilizado já existe"
    elif register_state == "ok":
        message = "Usuário criado"
    else:
        message
    
    register = dbc.Card([
        html.Div([
            html.H3("Registro"),
        ], style={"padding": "5px", "justify-content": "center", "display": "flex"}),
        html.Div([
            dbc.Input(id="user_register", placeholder="Usuário", type="text", style={"margin-bottom": "10px"}),
            dbc.Input(id="password_register", placeholder="Senha", type="password", style={"margin-bottom": "10px"}),
            dbc.Input(id="email_register", placeholder="Email", type="email", style={"margin-bottom": "10px"}),
            dcc.Dropdown(id="dropdown_registro", placeholder="Permissão de usuário", options=["aprop_admin", "aprop_operador", "lab_pcp", "lab_sgs"], style={"margin-bottom": "10px"}),
            dbc.Button("Registrar", id="register_button", style={"margin-bottom": "10px"}),
            dbc.Button("Voltar", id="botao_voltar")
        ], style={"display": "flex", "flex-direction": "column", "justify-content": "space-evenly", "padding": '10px', 'margin': "10px"}),
        
        html.Span(message, style={"text-align": 'center'}),

    ], style=card_style)

    return register

@app.callback(
    Output('register_state', 'data'),
    Input('register_button', 'n_clicks'),
    Input('botao_voltar', 'n_clicks'),
    [
        State('user_register', 'value'),
        State('password_register', 'value'),
        State('email_register', 'value'),
        State("dropdown_registro", "value")
    ]
)
@admin_required
def registrar_usuario(n_clicks, n_clicks2, user_register, password_register, email_register, role_register):
    if n_clicks is not None:
        if(user_register and password_register and email_register) is not None:
            with sqlite3.connect("dados.sqlite") as conn:
                ins_verify = f"SELECT * FROM usuarios WHERE nm_usr = '{user_register}' OR email_usr = '{email_register}';"
                cursor = conn.cursor()
                cursor.execute(ins_verify)
                rst = cursor.fetchone()
                if rst == None:
                    user = user_register
                    pwd = generate_password_hash(password_register, method="SHA256")
                    email = email_register
                    role = role_register
                    ins = f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('{user}', '{pwd}', '{email}', '{role}')"
                    cursor.execute(ins)

                    return "ok"
                else:
                    return "error_usuario_existente"
        else:
            return "error_info"
    if n_clicks2 is not None:
        return  ""

    # if n_clicks is not None:
    #     try:
    #         if (user_register is None) or (password_register is None) or (email_register is None):
    #             return 'error_info'
    #         elif (user_register and password_register and email_register) is not None:
    #             hashed_password = generate_password_hash(password_register, method="SHA256")
    #             ins = Users_table.insert().values(nm_usr=user_register, pwd_usr=hashed_password, email_usr=email_register, usr_role=role_register)
    #             # print(ins)
    #             # ins = f"insert into usuarios (nm_usr, email_usr, pwd_usr) values ('{user_register}', '{email_register}', '{hashed_password}')"
    #             conn = engine.connect()
    #             conn.execute(ins)
    #             conn.commit()
    #             conn.close()
    #             return ''
    #     except:
    #         return 'error_usuario_existente'
    # if n_clicks2 is not None:
    #     return ''


   