from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash

from app import *

from pages import login, register, home, consultar_paradas, consultar_turno, aprop_paradas, aprop_turno, atualizar_parada
from flask_login import current_user, logout_user
from sqlalchemy.orm import Session

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Location(id="base_url", refresh=False),
            dcc.Store(id="login_state", data=""),
            dcc.Store(id="register_state", data=""),

            html.Div(id="page_content", style={"height": "100vh", 'display': 'flex', 'justify-content': 'center', 'background-color': '#298753', 'width': '100vw'}), 
        ])
    ], style={'width': '100vw', 'height': '100vh'})
], style={'width': '100vw', 'height': '100vh'})

@login_manager.user_loader
def load_user(user_id):
    with Session(engine) as session:
        user = session.get(User, user_id)
        return user
    # return User.query.get(int(user_id))

@app.callback(
    Output("base_url", "pathname"),
    Input("login_state", "data"),
    Input("register_state", "data")
)
def atualizar_pathname(login_state, register_state):
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigg_id == 'login_state' and login_state == 'success':
            return '/home'

        if trigg_id == 'login_state' and (login_state == 'error' or login_state == 'error_senha'):
            return '/login'

        if trigg_id == 'register_state':
            if register_state == '':
                return '/home'
            else:
                return '/register'

@app.callback(
    Output("page_content", "children"),
    Input("base_url", "pathname"),
    [
        State('login_state', 'data'),
        State('register_state', 'data')
    ]
)
def renderizar_paginas(pathname, login_state, register_state):
    if pathname == "/login" or pathname == "/":
        return login.render_layout(login_state)

    if pathname == "/register":
        if current_user.usr_role == "admin":
            return register.render_layout(register_state)
        else:
            return home.render_layout(current_user)

    if pathname == '/home':
        if current_user.is_authenticated:
            return home.render_layout(current_user)
        else:
            return login.render_layout(register_state)

    if pathname == '/consultar_paradas':
        if current_user.is_authenticated:
            return consultar_paradas.render_layout(current_user)
        else:
            return login.render_layout(register_state)

    if pathname == '/consultar_turno':
        if current_user.is_authenticated:
            return consultar_turno.render_layout(current_user)
        else:
            return login.render_layout(register_state)

    if pathname == '/aprop_paradas':
        if current_user.is_authenticated:
            return aprop_paradas.render_layout(current_user)
        else:
            return login.render_layout(register_state)

    if pathname == '/aprop_turno':
        if current_user.is_authenticated:
            return aprop_turno.render_layout(current_user)
        else:
            return login.render_layout(register_state)

    if pathname == "/logout":
        if current_user.is_authenticated:
            logout_user()
            return login.render_layout(register_state)
        else:
            return login.render_layout(register_state)

    if '/atualizar_parada/' in pathname:
        if current_user.is_authenticated:
            id = pathname[18:]
            return atualizar_parada.render_layout(current_user, id)
        else:
            return login.render_layout(register_state)
            
if __name__ == "__main__":
    app.run_server(port=5000, debug=True)