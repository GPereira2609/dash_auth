import dash_bootstrap_components as dbc

from dash import html, dash

sidebar = dbc.Nav(
            [
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
            ],
            vertical=False,
            pills=True,
            class_name="text-center border",
            justified=True,
            fill=True,
            style={"position": "fixed"}
)