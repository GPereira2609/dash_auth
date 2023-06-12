from app import *
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import logout_user, current_user
from sqlalchemy import text
from functools import wraps

from globals import *
from pages import navbar

card_style = {
    "width": "45%",
    "height": "90%",
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'row',
    "justify-content": "center",
    "padding": "5%",
    "margin": "5%"
}

card_style2 = {
    "width": "55%",
    "height": "90%",
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'row',
    "justify-content": "center",
    "padding": "5%",
    "margin": "5%"
}

content = html.Div([

    dbc.Card([
        dbc.Col([
            dcc.Dropdown(["Via Seca", "Via Umida"], placeholder="Processo"),
            dcc.Dropdown(["Moagem", "Flotação"], placeholder="Sistema"),
            dcc.Dropdown(["2201-BF-001"], placeholder="Equipamento"),
            dcc.Dropdown(["Id", "Validade", "DataInicio", "DataFim", "Turno"], value=["Id", "DataFim", "Turno"], multi=True)
    ], style={"margin": "5%", "width": "90%"}),

        dbc.Col([
            dcc.Dropdown(["Horas Paradas HP", "Horas Manutenção HM"], placeholder="Tipo de código"),
            dcc.Dropdown(["Horas Paradas Externas HPE"], placeholder="Grupo de código"),
            dcc.Dropdown(["Parada Externa"], placeholder="Código das falhas"),
            dcc.Dropdown(["Condiões do tempo"], placeholder="Causa aparente"),
            dcc.Dropdown(["Outros"], placeholder="Componente")
    ], style={"margin": "5%", "width": "90%"}),

        dbc.Col([
            dcc.DatePickerSingle(placeholder="Data Início"),
            dcc.DatePickerSingle(placeholder="Data Fim"),
            dcc.Dropdown(["1º turno", "2º turno"], placeholder="Turno"),
            dbc.Button("Consultar")
        ], style={"margin": "5%", "width": "90%"}),
    ], style=card_style),

    dbc.Card([
        dash_table.DataTable(data=[{"teste1": f"dado{i}", "teste2": f"dado{i}", "teste3": f"dado{i}", "teste4": f"dado{i}"} for i in range(0, 100)], style_table={"height": '100%', "width": "100%", 'overflowY': 'auto'}, editable=True)
    ], style=card_style2)
    
], style={"width": "100%", "height": "100%", "display": "flex", "flex-diretion": "row", "justify-content": "center"})

def render_layout(user):
    username = user.nm_usr

    layout = html.Div([
        dcc.Location(id="page_teste", refresh=True),
        navbar.nav()[0],
            dbc.Row([   
                content
        ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
    ], style={'background-color': "white", 'height': '100vh', 'width': '100vw'})

    return layout