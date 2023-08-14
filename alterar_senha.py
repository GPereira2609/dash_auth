from dash import html, Input, Output, State, dcc
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from flask_login import current_user, logout_user
from app import *

import sqlite3
import dash_bootstrap_components as dbc
import time

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
    alter = dbc.Card([
        dcc.Location(id="base_url_alter", refresh=True),
            html.Div([
                html.Img(src=app.get_asset_url("mvv-logo.png"), height=70, width=180),
            ], style={"padding": "5px", "justify-content": "center", "display": "flex"}),
            html.Div([
                dbc.Input(id="user_pwd", placeholder="Senha atual", type="text", style={"margin-bottom": '10px'}),
                dbc.Input(id="password1", placeholder="Nova senha", type="password", style={"margin-bottom": '10px'}),
                dbc.Input(id="password2", placeholder="Repita a nova senha", type="password", style={"margin-bottom": '10px'}),
                dbc.Button("Alterar senha", id="alter_button"),
            ], style={'display': 'flex', "flex-direction": 'column', 'justify-content': 'space-evenly', "margin": "10px", "padding": "10px"}),
            
            html.Span(message, style={"text-align": 'center'}, id="span_alter"),
        
        ], style=card_style)
    
    return alter

@app.callback(
    Output("span_alter", "children"),
    Input("alter_button", "n_clicks"),
    State("user_pwd", "value"),
    State("password1", "value"),
    State("password2", "value"),
    prevent_initial_call=True
)
def verificar_senha(n, senha_antiga, senha_nova, senha_nova2):
    if n:
        if(check_password_hash(current_user.pwd_usr.replace("'", ""), senha_antiga)):
            if senha_nova and senha_nova2:
                if(senha_nova == senha_nova2):   
                    conn = sqlite3.connect("dados.sqlite")
                    cursor = conn.cursor()
                    hashed_pwd = generate_password_hash(password=senha_nova, method="SHA256")
                    ins = f"UPDATE usuarios SET pwd_usr = '{hashed_pwd}' WHERE id_usr = {current_user.id_usr};"
                    cursor.execute(ins)
                    conn.commit()
                    conn.close()

                    return "Senha alterada"
                else:
                    return "As senhas precisam ser iguais"
            else:
                return "Preencha todos os campos"
        else:
            return  "Senha incorreta"
        
@app.callback(
    Output("base_url_alter", "pathname"),
    Input("span_alter", "children")
)
def recarregar_pos_alteracao(msg):
    time.sleep(1.5)
    return "/" if msg == "Senha alterada" else "/alter_pwd"