import dash_bootstrap_components as dbc
from dash import html, dcc
from app import *

def nav():
    nav = dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                        dbc.Col([html.Div([
                            html.Img(src=app.get_asset_url('f2711217-e0a9-4a63-a24c-3c969b7ce090.png'), id="img_logo", className="w-16 md:w-32 lg:w-48", style={"height": "15%", "width": "15%"})

                        ], style={"margin-left": "5", "display": "flex", "flex-direction": "column", "justify-content": "center"})], style={"margin-left": "0 auto", "width": "50%"}),

                        dbc.Col([
                            # html.Div([
                            dbc.Nav([
                                dbc.NavLink("Home", href="/home", active="exact"),

                                dbc.DropdownMenu([
                                    dbc.NavLink("Consultar paradas", href="/consultar_paradas", active="exact"),
                                    dbc.NavLink("Apropriar paradas", href="/aprop_paradas", active="exact"),
                                    dbc.NavLink("Consultar turno", href="/consultar_turno", active="exact"),
                                    dbc.NavLink("Apropriação turno", href="/aprop_turno", active="exact"),
                                ], label="Apropriações", nav=True),

                                dbc.DropdownMenu([
                                    dbc.NavLink("MPAES", href="/lab/mpaes", active="exact"),
                                    dbc.NavLink("RAIO-X", href="/lab/raiox", active="exact")
                                ], label="Laboratório", nav=True),

                                dbc.DropdownMenu([
                                    dbc.NavLink("Registrar usuário", href="/register", active="exact"),
                                    dbc.NavLink("Sair", href="/logout")
                                ], label="Usuário", nav=True),
                            ], pills=True, vertical=False, id='nav')
                        # ], style={"height": "100%", 'display': 'flex', 'flex-direction': 'row'}),
                        ],style={"margin-right": "0 auto", "width": "50%", "display": "flex", "flex-direction": "column", "justify-content": "flex-end"})

                    ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-evenly'}),
                
                    ], style={"margin-left": "5px", "height": "100%", "display": "flex", "flex-direction": "column", "justify-content": "center"})
                ], style={"display": "flex", "flex-direction": "column", "justify-content": "space-between"})
                    
                ], style={"height": '10%', 'width': '105vw', 'display': 'flex', "flex-direction": "row", 'background-color': '#298753'}),
    return nav
